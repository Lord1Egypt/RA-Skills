#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_image_api.py —— 出图接口连通性自检（MV 版）。

用最短链路验证「NewAPI 图片中转」可用（④ 出图官跑批量出图前先跑这个）：

  1. GET  {base}/models              —— 验 key 与连通性，列可用模型
  2. POST {base}/images/generations  —— 用测试提示词真出一张，落盘并校验（PNG/JPEG 头 + 尺寸）

配置优先级：--base-url/--key/--model ＞ 环境变量 NEWAPI_IMAGE_* ＞ scripts/config.json ＞ 内置默认。

用法：
  python3 scripts/test_image_api.py                       # 用 config.json 跑全套
  python3 scripts/test_image_api.py --size 1536x1152      # 4:3 出图尺寸（MV 默认画幅）
  python3 scripts/test_image_api.py --quality medium      # 提高画质再测
  python3 scripts/test_image_api.py --base-url https://xxx --key sk-xxx --model xxx

⚠️ 第 2 步会**真调付费接口**出一张图（--quality low 已是最省）。
"""
from __future__ import annotations

import argparse
import base64
import json
import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import SKILL_ROOT, image_api_config  # noqa: E402

OUT_DIR = SKILL_ROOT / "assets" / "api_test"
TEST_PROMPT = ("a warm red lantern glowing on a pure white background, "
               "minimal flat illustration")


def normalize_base(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    if not u:
        return ""
    return u if u.endswith("/v1") else u + "/v1"


def http_json(url: str, key: str, payload: dict | None = None, timeout: int = 60):
    """GET（payload=None）或 POST JSON，返回 (status, obj_or_text)。"""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Authorization", "Bearer " + key)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            try:
                return resp.status, json.loads(body.decode("utf-8"))
            except Exception:  # noqa: BLE001
                return resp.status, body
    except urllib.error.HTTPError as exc:
        body = exc.read()
        try:
            return exc.code, json.loads(body.decode("utf-8"))
        except Exception:  # noqa: BLE001
            return exc.code, body
    except Exception as exc:  # noqa: BLE001
        return 0, str(exc)


def image_size(raw: bytes) -> tuple[int, int] | tuple[None, None]:
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", raw[16:24])
        return w, h
    if raw[:2] == b"\xff\xd8":  # JPEG：扫 SOF 段
        i = 2
        while i + 9 < len(raw):
            if raw[i] != 0xFF:
                i += 1
                continue
            marker = raw[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                h, w = struct.unpack(">HH", raw[i + 5:i + 9])
                return w, h
            seg_len = struct.unpack(">H", raw[i + 2:i + 4])[0]
            i += 2 + seg_len
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser(description="NewAPI 图片接口连通性测试（MV）")
    ap.add_argument("--base-url", default="", help="接口地址（默认 scripts/config.json）")
    ap.add_argument("--key", default="", help="API key（默认 scripts/config.json）")
    ap.add_argument("--model", default="", help="模型名（默认 scripts/config.json）")
    ap.add_argument("--size", default="1024x1024", help="测试出图尺寸（MV 4:3 用 1536x1152）")
    ap.add_argument("--quality", default="low", help="测试出图质量（默认 low，快且省）")
    ap.add_argument("--prompt", default=TEST_PROMPT, help="测试提示词")
    ap.add_argument("--timeout", type=int, default=300, help="出图请求超时秒数（默认 300）")
    args = ap.parse_args()

    cfg = image_api_config()
    base = normalize_base(args.base_url or cfg["base_url"])
    key = args.key or cfg["key"]
    model = args.model or cfg["model"]

    if not key:
        sys.exit("[FAIL] 未提供 key（--key / NEWAPI_IMAGE_KEY / scripts/config.json）")
    print(f"[配置] base={base}  model={model}  key={key[:8]}…{key[-4:]}")

    print("\n[1/2] GET /models …")
    status, obj = http_json(f"{base}/models", key, timeout=30)
    if status != 200:
        print(f"  ✗ HTTP {status}：{str(obj)[:300]}")
        print("  → key 无效 / 地址不对 / 网络不通；确认 base 是 NewAPI 中转地址（如 https://your-image-api.example.com）")
        return 1
    ids = [m.get("id") for m in obj.get("data", [])] if isinstance(obj, dict) else []
    print(f"  ✓ HTTP 200，可用模型：{ids if ids else obj}")

    print(f"\n[2/2] POST /images/generations …（size={args.size}，约 20–120 秒）")
    payload = {"model": model, "prompt": args.prompt, "size": args.size}
    if args.quality:
        payload["quality"] = args.quality
    t0 = time.time()
    status, obj = http_json(f"{base}/images/generations", key, payload=payload, timeout=args.timeout)
    dt = time.time() - t0
    if status != 200:
        print(f"  ✗ HTTP {status}（{dt:.1f}s）：{str(obj)[:400]}")
        return 1
    data = obj.get("data") if isinstance(obj, dict) else None
    if not data:
        print(f"  ✗ 响应里没有 data：{str(obj)[:400]}")
        return 1
    item = data[0]
    if item.get("b64_json"):
        raw = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as resp:
            raw = resp.read()
    else:
        print(f"  ✗ 响应字段无法识别：{list(item.keys())}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"test_{time.strftime('%Y%m%d_%H%M%S')}.png"
    out.write_bytes(raw)
    w, h = image_size(raw)
    print(f"  ✓ HTTP 200（{dt:.1f}s）· {len(raw)} bytes · {w}x{h}")
    print(f"  ✓ 测试图已保存：{out}")
    print("\n[OK] 接口连通、key 有效、出图成功。批量出图：python3 scripts/generate_images.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
