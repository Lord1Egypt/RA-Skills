#!/usr/bin/env python3
"""
scripts/maigret_client.py — Maigret 身份归因客户端（M0.3，默认 OFF）

Maigret（soxoj/maigret，Sherlock fork）：用户名 → 全平台账号足迹发现
（3000+ 站点，递归搜索、profile 解析、关系图谱、ML 降误报）。

设计要点：
  - 默认 OFF：须经注册表 enabled ∩ consent 双闸口才运行（合规优先）
  - 懒加载 + subprocess 调用 CLI（隔离重依赖于主进程；不 import maigret 进 infoseek）
  - 错误分类复用 engine_lifecycle.classify（经 core.capability_errors.CapabilityError.code）
  - 无 key 需求；仅处理公开数据；opt-in
  - 结果回写 infoseek 锚点矩阵"身份归因平面 B"

安全/合规：
  - requires_consent=true → 未授权抛 ConsentRequired，绝不静默运行
  - 不递归、不抓个人页（默认 --no-recursion --no-extracting，仅存在性）

────────────────────────────────────────────────────────────────────────
CLI 契约（maigret 0.6.x 实测，2026-09-18 沙箱实证）
────────────────────────────────────────────────────────────────────────
旧实现三处与真实 CLI 不符，导致在真实环境必然落空：
  1. ``--json`` 不存在；正确是 ``-J TYPE/--json TYPE``，且 TYPE ∈
     {simple, ndjson}，是**报告类型**，报告写文件**不进 stdout**；
  2. ``--print-found-only`` / ``--skip-existing`` 参数不存在；
     ``-a`` 是「全量站点扫描」而非"限定站点数"（限站点用 --top-sites N）；
  3. simple JSON 真实结构是 ``{site_name: {..., "status": {dict}}}``——
     status 是**嵌套 dict**（含 status:"Claimed"/url/username/ids/tags），
     不是字符串；旧解析找 data["sites"] 列表必然为空。

正确契约（本模块采用）：
  maigret <user> -J simple --no-recursion --no-extracting
                  --top-sites N --timeout T
    - 报告文件：<cwd>/reports/report_<user>_simple.json
    - 结构：{site: {"url_user","rank","username","status": {
              "status":"Claimed","url":...,"ids":{},"tags":[...]}}}
    - --top-sites N：按 Alexa 排名取前 N 站（CLI 对小值钳制，实测最小 10）；
      0/缺省可能触发全量 2500+ 站，故本模块恒显式传一个受控上限。
本模块在临时工作目录运行，glob 回读唯一 simple 报告，避免用户名文件名字符问题。
"""

from __future__ import annotations

import json
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import Dict, List

log = logging.getLogger("infoseek.maigret")

try:
    from core.capability_errors import CapabilityError, ConsentRequired, CapabilityUnavailable
    from core.capability_registry import (
        get_capability, grant_consent, is_effective_enabled, is_enabled,
        requires_consent,
    )
except ImportError:  # 直接运行时兜底
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "core"))
    from capability_errors import CapabilityError, ConsentRequired, CapabilityUnavailable
    from capability_registry import (
        get_capability, grant_consent, is_effective_enabled, is_enabled,
        requires_consent,
    )

CAP_NAME = "Maigret"

_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _core = str(pathlib.Path(__file__).resolve().parent.parent / "core")
        if _core not in sys.path:
            sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr

# top-sites 受控上限：默认只扫高排名站点以控耗时/降误报。
# 注意 maigret 对过小值会钳制（实测 min≈10）；显式全量须 recursive/调用方指定。
DEFAULT_TOP_SITES = 100


def _resolve_cli() -> List[str]:
    """定位 maigret 可执行：PATH → 隔离 venv（INFOSEEK_MAIGRET_VENV）。

    返回命令片段（list，如 ['/venv/bin/maigret'] 或 ['/venv/python','-m','maigret']），
    调用方以 cli + [username, ...] 拼接，避免 Windows 模块式回退出现含空格的单字符串。
    """
    cli = _dep_reg().which_path("maigret")
    if cli:
        return [cli]
    venv = os.environ.get("INFOSEEK_MAIGRET_VENV")
    if venv:
        scripts = pathlib.Path(venv) / ("Scripts" if sys.platform == "win32" else "bin")
        for name in ("maigret", "maigret.exe"):
            cand = scripts / name
            if cand.exists():
                return [str(cand)]
        # 退回模块式调用（隔离 venv 的 python -m maigret）
        py = scripts / ("python.exe" if sys.platform == "win32" else "python")
        if py.exists():
            return [str(py), "-m", "maigret"]
    return ["maigret"]


def _consent_gate(consent: bool) -> None:
    if requires_consent(CAP_NAME):
        if consent:
            grant_consent(CAP_NAME)
        else:
            # 即便注册表声明启用，未授权也禁止运行
            if not is_effective_enabled(CAP_NAME):
                raise ConsentRequired(CAP_NAME)


def search(username: str,
           consent: bool = False,
           max_sites: int = DEFAULT_TOP_SITES,
           recursive: bool = False,
           timeout: int = 180,
           no_extract: bool = True) -> List[Dict]:
    """对公开用户名做身份归因发现（默认存在性，不递归/不抓个人页）。

    返回账号列表：{platform, url, username, fullname, site_rank,
                   http_status, confidence, source, ids, tags}
    未启用 → []（安全降级）；未授权/CLI 缺失 → 上抛由 search_web/pipeline 捕获。
    """
    # 1) 默认 OFF 闸口
    if not is_enabled(CAP_NAME):
        log.debug(f"[{CAP_NAME}] 未启用（默认 OFF），跳过")
        return []
    # 2) 合规闸口（未授权上抛 ConsentRequired，由 search_web / pipeline 捕获降级）
    _consent_gate(consent)

    cli = _resolve_cli()
    # 0.6.x 契约：-J simple 写报告文件；限站点用 --top-sites（非 -a）
    cmd = cli + [username, "-J", "simple", "--timeout", str(max(5, int(timeout)))]
    if not recursive:
        cmd.append("--no-recursion")
    if no_extract:
        cmd.append("--no-extracting")
    # max_sites<=0 表示调用方显式全量（-a）；否则受控 top-sites。
    if max_sites and max_sites > 0:
        cmd += ["--top-sites", str(max_sites)]

    with tempfile.TemporaryDirectory(prefix="infoseek_maigret_") as workdir:
        try:
            proc = subprocess.run(
                cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout)
        except FileNotFoundError:
            raise CapabilityUnavailable(CAP_NAME, "CLI 未安装（隔离 venv 未配置）")
        except subprocess.TimeoutExpired:
            raise CapabilityError(f"{CAP_NAME} 超时（>{timeout}s）", code=0)
        except Exception as e:
            raise CapabilityError(f"{CAP_NAME} 执行异常: {e}", code=0, cause=e)

        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "").strip()
            # maigret 偶发非零退出但仍有部分结果；尝试读报告文件
            log.warning(f"[{CAP_NAME}] CLI 返回 {proc.returncode}: {err[:200]}")

        # 报告：<cwd>/reports/report_<user>_simple.json；用户名可能含特殊字符，glob 兜底。
        reports = sorted(pathlib.Path(workdir).rglob("*_simple.json"))
        if not reports:
            log.debug(f"[{CAP_NAME}] 无 simple 报告产物（可能 0 命中或 CLI 异常）")
            return []
        try:
            data = json.loads(reports[0].read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError as e:
            log.warning(f"[{CAP_NAME}] 报告 JSON 解析失败: {e}")
            return []

    return _parse_simple(data, username)


def _parse_simple(data: object, queried_username: str = "") -> List[Dict]:
    """解析 maigret simple 报告（0.6.x 实测 schema）。

    结构：{site_name: {
        "site": {...站点定义...}, "url_user": ..., "rank": int,
        "username": ..., "http_status": int,
        "status": {"username","site_name","url","status":"Claimed",
                   "ids":{},"tags":[...], "keyword_match_status":...}
    }}
    仅纳入嵌套 status.status == "Claimed" 且有 URL 的条目。
    兼容旧/变异：status 为字符串的 ndjson 风格也尝试接受。
    """
    out: List[Dict] = []
    if not isinstance(data, dict):
        return out
    for site_name, entry in data.items():
        if not isinstance(entry, dict):
            continue
        status_obj = entry.get("status")
        # 新 schema：status 是嵌套 dict
        if isinstance(status_obj, dict):
            state = (status_obj.get("status") or "").strip()
            url = status_obj.get("url") or entry.get("url_user") or ""
            uname = status_obj.get("username") or entry.get("username") or queried_username
            ids = status_obj.get("ids") or {}
            tags = status_obj.get("tags") or []
        elif isinstance(status_obj, str):
            # 兼容 ndjson/旧风格扁平条目
            state = status_obj.strip()
            url = entry.get("url_user") or entry.get("url") or ""
            uname = entry.get("username") or queried_username
            ids = entry.get("ids") or {}
            tags = entry.get("tags") or []
        else:
            continue
        if state != "Claimed" or not url:
            continue
        try:
            rank = int(entry.get("rank") or 0)
        except (TypeError, ValueError):
            rank = 0
        try:
            http_status = int(entry.get("http_status") or 0)
        except (TypeError, ValueError):
            http_status = 0
        out.append({
            "platform": site_name or status_obj.get("site_name") if isinstance(status_obj, dict) else site_name,
            "url": url,
            "username": uname or "",
            "fullname": "",
            "site_rank": rank,
            "http_status": http_status,
            "confidence": 0.9,
            "source": CAP_NAME,
            "ids": ids if isinstance(ids, dict) else {},
            "tags": tags if isinstance(tags, list) else [],
        })
    return out


# 模块级便捷封装（供 pipeline 调用；consent 默认 False 安全）
def search_web(username: str, **kw) -> List[Dict]:
    try:
        return search(username, **kw)
    except (ConsentRequired, CapabilityUnavailable, CapabilityError):
        return []
