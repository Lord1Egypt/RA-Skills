#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prana 封装技能 — 薄客户端（无业务逻辑，仅负责与 Prana 服务通信）
从 GitHub / Claw Hub 等下载本技能包后，通过本脚本将用户输入转发到 Prana 执行真实能力。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# 技能根目录（本脚本位于 scripts/ 下）
SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_ROOT / "config"
API_KEY_FILE = CONFIG_DIR / "api_key.txt"
API_KEY_JSON_FILE = CONFIG_DIR / "api_key.json"
SKILL_MD_FILE = SKILL_ROOT / "SKILL.md"

DEFAULT_PRANA_BASE = os.environ.get("NEXT_PUBLIC_URL", "https://suna-dev.ebonex.io")

# agent-run 为长连接场景；超时或失败后改查 agent-result（同一 request_id）
HTTP_TIMEOUT_SEC = 120


def _extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    if not content.strip().startswith("---"):
        return None, content
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return None, content
    try:
        import yaml

        fm = yaml.safe_load(match.group(1))
        return (fm if isinstance(fm, dict) else None), match.group(2)
    except Exception:
        return None, content


def load_skill_config() -> Dict[str, Any]:
    """
    从技能包根目录 SKILL.md 的 YAML frontmatter 读取配置。
    - original_skill_key：Prana 上实际执行的专业技能（agent-run body 使用）。
    - skill_key：公开包标识（一般为 源 key + _public）；若缺 original_skill_key 则回退仅用 skill_key（旧包）。
    """
    if not SKILL_MD_FILE.exists():
        print(
            "错误: 未找到 SKILL.md，请使用完整封装技能包解压后运行。",
            file=sys.stderr,
        )
        sys.exit(1)
    raw = SKILL_MD_FILE.read_text(encoding="utf-8")
    frontmatter, _ = _extract_frontmatter(raw)
    if not frontmatter:
        print("错误: SKILL.md 缺少有效的 YAML frontmatter。", file=sys.stderr)
        sys.exit(1)
    original = str(frontmatter.get("original_skill_key") or "").strip()
    pub = str(frontmatter.get("skill_key") or "").strip()
    # 调用远端：优先 original_skill_key；兼容旧包仅含 skill_key（且为源 key）
    sk = original if original else pub
    if not sk:
        print(
            "错误: SKILL.md frontmatter 需包含 original_skill_key 与 skill_key（或旧包仅 skill_key）。",
            file=sys.stderr,
        )
        sys.exit(1)
    sip = ""
    for key in ("input_format", "input_schema", "params"):
        v = frontmatter.get(key)
        if v is not None and str(v).strip():
            sip = str(v).strip()[:16000]
            break
    if not sip:
        d = frontmatter.get("description")
        if d is not None and str(d).strip():
            sip = str(d).strip()[:8000]
    return {"skill_key": sk, "skill_invocation_params": sip}


def _parse_credentials_json(text: str) -> Optional[Tuple[str, str]]:
    """解析 GET /api/v1/api-keys/ 完整响应，或仅含 public_key / secret_key 的 JSON。"""
    t = text.strip()
    if not t.startswith("{"):
        return None
    try:
        obj = json.loads(t)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    data = obj.get("data")
    ak = None
    if isinstance(data, dict):
        ak = data.get("api_key")
    if isinstance(ak, dict) and ak.get("public_key") and ak.get("secret_key"):
        return str(ak["public_key"]).strip(), str(ak["secret_key"]).strip()
    ak = obj.get("api_key")
    if isinstance(ak, dict) and ak.get("public_key") and ak.get("secret_key"):
        return str(ak["public_key"]).strip(), str(ak["secret_key"]).strip()
    if obj.get("public_key") and obj.get("secret_key"):
        return str(obj["public_key"]).strip(), str(obj["secret_key"]).strip()
    return None


def _parse_credentials_line(line: str) -> Optional[Tuple[str, str]]:
    """单行 public_key:secret_key（取首个冒号分割，避免密钥中含冒号时误拆）。"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if ":" not in line:
        return None
    pub, _, sec = line.partition(":")
    pub, sec = pub.strip(), sec.strip()
    if pub and sec:
        return pub, sec
    return None


def _headers_x_api_key(public_key: str, secret_key: str) -> dict[str, str]:
    """Claw 接口要求：x-api-key 为 public_key:secret_key。"""
    return {
        "Content-Type": "application/json",
        "x-api-key": f"{public_key}:{secret_key}",
    }


def load_prana_credentials() -> Tuple[str, str]:
    """
    从环境变量或配置文件读取 public_key、secret_key（来自 GET /api/v1/api-keys/ 返回的 data.api_key）。
    获取 Key 时可选查询参数 account_id；沙盒可从环境变量 ACCOUNT_ID 传入，无则省略。
    优先级：
      PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY
      PRANA_SKILL_API_KEY（整段 JSON，或单行 public_key:secret_key）
      config/api_key.json
      config/api_key.txt（JSON 或单行 public_key:secret_key）
    """
    pk = os.environ.get("PRANA_SKILL_PUBLIC_KEY", "").strip()
    sk = os.environ.get("PRANA_SKILL_SECRET_KEY", "").strip()
    if pk and sk:
        return pk, sk

    raw = os.environ.get("PRANA_SKILL_API_KEY", "").strip()
    if raw:
        parsed = _parse_credentials_json(raw)
        if parsed:
            return parsed
        p = _parse_credentials_line(raw)
        if p:
            return p

    if API_KEY_JSON_FILE.exists():
        parsed = _parse_credentials_json(API_KEY_JSON_FILE.read_text(encoding="utf-8"))
        if parsed:
            return parsed

    if API_KEY_FILE.exists():
        txt = API_KEY_FILE.read_text(encoding="utf-8")
        lines = [ln for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        joined = "\n".join(lines).strip()
        if joined:
            parsed = _parse_credentials_json(joined)
            if parsed:
                return parsed
            for line in lines:
                p = _parse_credentials_line(line)
                if p:
                    return p

    print(
        "错误: 未配置 API 凭证（public_key + secret_key）。\n"
        "  1) 调用 Prana GET /api/v1/api-keys/（可选 account_id、phone、email；沙盒可设 ACCOUNT_ID 后带 ?account_id=…，无则省略），从返回 data.api_key 取得 public_key、secret_key。\n"
        "  2) 将完整 JSON 写入 config/api_key.json，或单行 public_key:secret_key 写入 config/api_key.txt；\n"
        "     或设置 PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY，或 PRANA_SKILL_API_KEY（JSON 或 pk:sk 单行）。",
        file=sys.stderr,
    )
    sys.exit(2)


def build_invoke_content(cfg: dict, user_message: str) -> str:
    """
    组装请求 question：参数说明 + 用户消息。
    skill_key 来自 SKILL.md frontmatter，由调用方单独传入 HTTP body。
    """
    params_from_skill = (cfg.get("skill_invocation_params") or "").strip()
    lines = [
        f"参数：{params_from_skill}",
        f"用户消息：{user_message}",
    ]
    return "\n".join(lines)


def fetch_agent_result(
    base_url: str,
    request_id: str,
    public_key: str,
    secret_key: str,
) -> dict:
    """
    当 agent-run 超时或失败时，用同一 request_id 查询运行结果。
    POST /api/claw/agent-result  body: request_id（鉴权见 x-api-key）
    Header: x-api-key: public_key:secret_key
    """
    url = base_url.rstrip("/") + "/api/claw/agent-result"
    body = {"request_id": request_id}
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers_x_api_key(public_key, secret_key),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(err_body)
        except json.JSONDecodeError:
            return {
                "error": True,
                "status": e.code,
                "detail": err_body,
                "_from": "agent-result",
            }
    except urllib.error.URLError as e:
        return {"error": True, "detail": str(e.reason), "_from": "agent-result"}


def _mark_recovered(d: dict) -> dict:
    d = dict(d)
    d["_recovered_via"] = "agent-result"
    return d


def invoke_prana(
    base_url: str,
    skill_key: str,
    content: str,
    thread_id: str | None,
    request_id: str,
    public_key: str,
    secret_key: str,
) -> dict:
    """
    调用 Prana 技能执行接口。
    body: skill_key, question, thread_id, request_id（不含 api_key）
    Header: x-api-key: public_key:secret_key
    若 HTTP 超时、连接失败，或网关类错误（5xx / 408 / 504），则改调 agent-result 用 request_id 取结果。
    """
    url = base_url.rstrip("/") + "/api/claw/agent-run"
    body = {
        "skill_key": skill_key,
        "question": content,
        "thread_id": thread_id or "",
        "request_id": request_id,
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers_x_api_key(public_key, secret_key),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except json.JSONDecodeError:
        return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        # 网关/服务端错误或超时类状态：任务可能已在服务端执行，改查 agent-result
        if e.code >= 500 or e.code in (408, 504):
            return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))
        try:
            return json.loads(err_body)
        except json.JSONDecodeError:
            return {"error": True, "status": e.code, "detail": err_body}
    except urllib.error.URLError:
        # 含连接失败、DNS、超时等
        return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))
    except TimeoutError:
        return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 Prana 远程技能服务")
    parser.add_argument("--message", "-m", required=True, help="用户消息 / 任务描述")
    parser.add_argument("--thread-id", "-t", default="", help="对话 thread_id，首轮可留空")
    parser.add_argument("--base-url", "-b", default=DEFAULT_PRANA_BASE, help="Prana API 根地址")
    args = parser.parse_args()

    cfg = load_skill_config()
    skill_key = cfg.get("skill_key") or ""
    if not skill_key:
        print("错误: 配置中缺少远端 skill_key（请检查 SKILL.md 的 original_skill_key）", file=sys.stderr)
        sys.exit(1)

    public_key, secret_key = load_prana_credentials()
    request_id = str(uuid.uuid4())
    content = build_invoke_content(cfg, args.message)
    result = invoke_prana(
        args.base_url,
        skill_key,
        content,
        args.thread_id or None,
        request_id,
        public_key,
        secret_key,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
