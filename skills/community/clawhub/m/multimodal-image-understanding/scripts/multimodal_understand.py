#!/usr/bin/env python3
"""
multimodal_understand.py — 调用上游支持多模态的大模型来理解图片。

支持的协议（通过 BYOK 配置中的 `protocol` 字段选择）：
  - anthropic : Anthropic Messages API（POST /v1/messages）
  - openai    : OpenAI Chat Completions API（POST /chat/completions）

配置从 JSON 文件读取（默认路径：~/.config/multimodal-image-understanding/config.json）。
所有字符串值支持 ${VAR} 形式的环境变量展开。

图片可以是本地文件路径（读取后 base64 编码）或 HTTP(S) URL（直接传递给支持 URL 的 provider；
若 provider 不支持，可在配置中设置 "image_mode": "base64"，脚本会先下载再编码）。

输出：模型回复文本打印到 stdout。带 --quiet 时只输出回复；不带时进度日志走 stderr，回复走 stdout。
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


# ---------- Config loading ----------

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "multimodal-image-understanding" / "config.json"

_ENV_VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _expand_env(value: Any) -> Any:
    """递归展开字符串值中的 ${VAR} 引用，从 os.environ 读取。"""
    if isinstance(value, str):
        def repl(m: re.Match) -> str:
            name = m.group(1)
            if name not in os.environ:
                raise SystemExit(f"错误：配置中引用的环境变量 {name!r} 未设置")
            return os.environ[name]
        return _ENV_VAR_RE.sub(repl, value)
    if isinstance(value, list):
        return [_expand_env(v) for v in value]
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    return value


def load_config(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(
            f"错误：找不到配置文件 {path}\n"
            f"提示：将 assets/config.example.json 复制到 {path} 并填入你的配置。"
        )
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise SystemExit(f"错误：无法读取配置文件 {path}：{e}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"错误：配置文件 {path} 不是合法 JSON：{e}")
    if not isinstance(data, dict):
        raise SystemExit("错误：配置文件根节点必须是 JSON 对象")
    return _expand_env(data)


# ---------- Image handling ----------

SUPPORTED_MIME = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def _guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if mime and mime in SUPPORTED_MIME:
        return mime
    # 按扩展名兜底
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    if ext == ".gif":
        return "image/gif"
    raise SystemExit(f"错误：无法识别 {path} 的 MIME 类型；仅支持 JPEG/PNG/WebP/GIF")


def _is_url(s: str) -> bool:
    return s.lower().startswith(("http://", "https://"))


def _download_url(url: str, timeout: int) -> tuple[bytes, str | None]:
    """下载 URL 内容，返回 (bytes, content_type_from_header)。"""
    req = urllib.request.Request(url, headers={"User-Agent": "multimodal-image-understanding/1.0"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        if resp.status != 200:
            raise SystemExit(f"错误：下载图片失败，HTTP {resp.status}")
        ct = resp.headers.get("Content-Type", "").split(";")[0].strip().lower() or None
        return resp.read(), ct


def _guess_mime_from_url(url: str, content_type: str | None = None) -> str:
    """从 URL 路径或 HTTP Content-Type header 推断 MIME 类型。"""
    # 优先使用 HTTP 响应头
    if content_type and content_type in SUPPORTED_MIME:
        return content_type
    mime, _ = mimetypes.guess_type(url)
    if mime and mime in SUPPORTED_MIME:
        return mime
    path = url.split("?", 1)[0]
    ext = Path(path).suffix.lower()
    ext_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
               ".webp": "image/webp", ".gif": "image/gif"}
    if ext in ext_map:
        return ext_map[ext]
    # 兜底：无法推断时默认为 JPEG
    return "image/jpeg"


def prepare_image(image: str, image_mode: str, timeout: int) -> dict:
    """
    返回与所选协议对应的图片内容块。

    image_mode 取值：
      - "auto"  ：--image 是 URL 时直接传 URL；是本地路径时 base64 编码
      - "url"   ：始终传 URL（本地路径会报错）
      - "base64"：始终先下载/读取再 base64 编码
    """
    if _is_url(image):
        if image_mode == "base64":
            data, content_type = _download_url(image, timeout=timeout)
            mime = _guess_mime_from_url(image, content_type)
            b64 = base64.standard_b64encode(data).decode("ascii")
            return {"source": "base64", "mime": mime, "data": b64, "url": None}
        return {"source": "url", "mime": None, "data": None, "url": image}

    # 本地文件
    path = Path(image).expanduser()
    if not path.exists():
        raise SystemExit(f"错误：找不到图片文件 {path}")
    if image_mode == "url":
        raise SystemExit("错误：--image 是本地路径，但配置中 image_mode='url'，请改为 auto 或 base64")
    data = path.read_bytes()
    if len(data) > 20 * 1024 * 1024:
        raise SystemExit(f"错误：图片 {path} 超过 20MB，请先压缩")
    mime = _guess_mime(path)
    b64 = base64.standard_b64encode(data).decode("ascii")
    return {"source": "base64", "mime": mime, "data": b64, "url": None}


# ---------- HTTP helper (stdlib only, no requests dependency) ----------

def _http_post_json(url: str, headers: dict, body: dict, timeout: int) -> dict:
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST", headers=headers)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise SystemExit(
            f"错误：上游返回 HTTP {e.code} {e.reason}\n{err_body}"
        )
    except urllib.error.URLError as e:
        raise SystemExit(f"错误：无法连接上游：{e.reason}")


# ---------- Anthropic protocol ----------

def _anthropic_headers(cfg: dict) -> dict:
    headers = {
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    if cfg.get("api_key"):
        if cfg.get("auth_header"):
            headers[cfg["auth_header"]] = cfg["api_key"]
        else:
            headers["x-api-key"] = cfg["api_key"]
    return {k: v for k, v in headers.items() if v}


def call_anthropic(cfg: dict, prompt: str, image: dict, timeout: int) -> str:
    endpoint = cfg["endpoint"].rstrip("/")
    url = f"{endpoint}/v1/messages"
    model = cfg["model"]
    max_tokens = int(cfg.get("max_tokens", 1024))
    temperature = cfg.get("temperature")

    # 组装 content blocks
    if image["source"] == "url":
        image_block = {
            "type": "image",
            "source": {"type": "url", "url": image["url"]},
        }
    else:
        image_block = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image["mime"],
                "data": image["data"],
            },
        }

    body: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    image_block,
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }
    if temperature is not None:
        body["temperature"] = float(temperature)
    # 可选：system prompt
    if cfg.get("system"):
        body["system"] = cfg["system"]

    resp = _http_post_json(url, _anthropic_headers(cfg), body, timeout)
    # 解析响应
    content = resp.get("content") or []
    parts = [c.get("text", "") for c in content if c.get("type") == "text"]
    text = "\n".join(p for p in parts if p).strip()
    if not text:
        # 兼容部分网关
        text = resp.get("completion") or ""
    return text


# ---------- OpenAI ChatCompletion protocol ----------

def _openai_headers(cfg: dict) -> dict:
    headers = {"content-type": "application/json"}
    if cfg.get("api_key"):
        if cfg.get("auth_header"):
            headers[cfg["auth_header"]] = cfg["api_key"]
        else:
            headers["Authorization"] = f"Bearer {cfg['api_key']}"
    return {k: v for k, v in headers.items() if v}


def call_openai(cfg: dict, prompt: str, image: dict, timeout: int) -> str:
    endpoint = cfg["endpoint"].rstrip("/")
    url = f"{endpoint}/chat/completions"
    model = cfg["model"]
    max_tokens = int(cfg.get("max_tokens", 1024))
    temperature = cfg.get("temperature")

    if image["source"] == "url":
        image_part = {"type": "image_url", "image_url": {"url": image["url"]}}
    else:
        image_part = {
            "type": "image_url",
            "image_url": {"url": f"data:{image['mime']};base64,{image['data']}"},
        }

    body: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    image_part,
                ],
            }
        ],
    }
    if temperature is not None:
        body["temperature"] = float(temperature)

    resp = _http_post_json(url, _openai_headers(cfg), body, timeout)
    choices = resp.get("choices") or []
    if not choices:
        raise SystemExit(f"错误：上游响应中没有 choices：{json.dumps(resp)[:500]}")
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        return content.strip()
    # 兼容部分 provider 把 content 返回为分段列表
    if isinstance(content, list):
        parts = [p.get("text", "") for p in content if p.get("type") in ("text", "output_text")]
        return "\n".join(p for p in parts if p).strip()
    return str(content).strip()


# ---------- Main ----------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="调用上游支持多模态的大模型来理解图片。"
    )
    parser.add_argument("--image", required=True, help="图片的本地路径或 HTTP(S) URL")
    parser.add_argument("--prompt", required=True, help="关于图片的 prompt/问题")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH,
                        help=f"BYOK 配置文件路径（默认：{DEFAULT_CONFIG_PATH}）")
    parser.add_argument("--protocol", choices=["anthropic", "openai"],
                        help="覆盖配置文件中的 protocol")
    parser.add_argument("--model", help="覆盖配置文件中的 model")
    parser.add_argument("--max-tokens", type=int, help="覆盖 max_tokens")
    parser.add_argument("--timeout", type=int, default=120, help="请求超时时间（秒）")
    parser.add_argument("--quiet", action="store_true",
                        help="关闭 stderr 上的进度日志，仅输出模型回复到 stdout")
    args = parser.parse_args(argv)

    def log(msg: str) -> None:
        if not args.quiet:
            print(msg, file=sys.stderr)

    log(f"[multimodal] 正在加载配置：{args.config}")
    cfg = load_config(args.config)

    # 应用 CLI 覆盖
    if args.protocol:
        cfg["protocol"] = args.protocol
    if args.model:
        cfg["model"] = args.model
    if args.max_tokens is not None:
        cfg["max_tokens"] = args.max_tokens

    # 校验
    protocol = (cfg.get("protocol") or "").lower()
    if protocol not in {"anthropic", "openai"}:
        raise SystemExit("错误：config.protocol 必须是 'anthropic' 或 'openai'")
    if not cfg.get("endpoint"):
        raise SystemExit("错误：config.endpoint 必填")
    if not cfg.get("model"):
        raise SystemExit("错误：config.model 必填")
    if not cfg.get("api_key") and not cfg.get("auth_header"):
        log("[multimodal] 警告：未设置 api_key，请求很可能会因 401 失败")

    log(f"[multimodal] 协议={protocol} 模型={cfg['model']} 端点={cfg['endpoint']}")

    image_mode = (cfg.get("image_mode") or "auto").lower()
    if image_mode not in {"auto", "url", "base64"}:
        raise SystemExit("错误：config.image_mode 必须是 auto / url / base64 之一")

    log(f"[multimodal] 准备图片（mode={image_mode}）")
    image = prepare_image(args.image, image_mode, args.timeout)

    log("[multimodal] 正在调用上游 API...")
    if protocol == "anthropic":
        reply = call_anthropic(cfg, args.prompt, image, args.timeout)
    else:
        reply = call_openai(cfg, args.prompt, image, args.timeout)

    if not reply:
        log("[multimodal] 警告：上游返回了空回复")
    print(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
