#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_images.py —— 30 秒说唱人物参考图出图（NewAPI 图片中转 · 原生支持参考图）。
API 不通时写 `04-图片/generate_image参数.json` 并退出 6（generate_image / edit_image 兜底 + --adopt 收位）。

读项目根目录的 `文生图提示词.json`，逐条调图片接口出图，按 `kind` 落到 `04-图片/<kind>/<id>.png`（与分镜 JSON 的 `refs_urls` 路径口径一致）。

两种行格式都吃：
  {"style": "...", "ratio": "4:3", "rows": [ {id, kind, prompt, refs, size}, ... ]}
  [ {id, kind, prompt, refs, size}, ... ]

成本纪律（铁律⑪）：
  · 默认**一次只出一张**（出完停下来核对，再跑一次出下一张）；
  · 不加 `--yes` 只预览、不调付费接口；
  · 要连出多张必须显式 `--all`（串行）或 `--batch`（并发，需同时给 `--concurrency`）。

用法：
  # 看要出哪些（不花钱）
  python3 scripts/generate_images.py --project assets/output/MV01-xiaoyu --dry-run
  # 出第一张（付费）｜出完再跑一次出下一张
  python3 scripts/generate_images.py --project assets/output/M01-xxx --yes
  # 指定某张 / 某风格
  python3 scripts/generate_images.py --project MV01-xxx --id ref_人物 --yes
  python3 scripts/generate_images.py --project MV01-xxx --kind "重彩水墨轻鎏金" --yes
  # 连出全部（串行）｜并发出图（明确解锁）
  python3 scripts/generate_images.py --project MV01-xxx --all --yes
  python3 scripts/generate_images.py --project MV01-xxx --batch --concurrency 2 --yes

配置优先级：--base-url/--key/--model ＞ 环境变量 NEWAPI_IMAGE_* ＞ scripts/config.json ＞ 内置默认。
参考图解析：`refs` 里的名字会递归扫项目 `04-图片/**`。
出完图后跑 `upload_project.py <项目> --verify`，写完 JSON 再 `--fill-only` 回填直链。
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    IMAGE_ROOT, find_ref_image, image_api_config, resolve_project,
)

IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")
RATIO_TO_SIZE = {"16:9": "1536x1024", "9:16": "1024x1536", "4:3": "1536x1152", "3:4": "1152x1536"}
DEFAULT_PROMPTS = "文生图提示词.json"


# ---------------------------------------------------------------- 接口

def normalize_base(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    if not u:
        return ""
    return u if u.endswith("/v1") else u + "/v1"


def _parse_image_response(obj: dict) -> bytes:
    if obj.get("error"):
        raise RuntimeError(f"接口报错: {str(obj['error'])[:300]}")
    data = obj.get("data") or []
    if not data:
        raise RuntimeError(f"响应无 data: {str(obj)[:300]}")
    item = data[0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=180) as r:
            return r.read()
    raise RuntimeError(f"响应字段无法识别: {list(item.keys())}")


def _post_json(url: str, key: str, payload: dict, timeout: int) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}")
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"网络错误: {exc}")


def _post_multipart(url: str, key: str, fields: list, files: list, timeout: int) -> dict:
    boundary = "----mv" + uuid.uuid4().hex
    buf: list[bytes] = []
    for name, value in fields:
        if value is None or value == "":
            continue
        buf.append(f"--{boundary}\r\n".encode())
        buf.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        buf.append(str(value).encode("utf-8"))
        buf.append(b"\r\n")
    for field, filename, blob in files:
        lower = filename.lower()
        ctype = ("image/png" if lower.endswith(".png")
                 else "image/jpeg" if lower.endswith((".jpg", ".jpeg")) else "image/webp")
        buf.append(f"--{boundary}\r\n".encode())
        buf.append((f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
                    f"Content-Type: {ctype}\r\n\r\n").encode())
        buf.append(blob)
        buf.append(b"\r\n")
    buf.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(url, data=b"".join(buf), method="POST")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}")
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"网络错误: {exc}")


def api_generate(base, key, model, prompt, size, quality, timeout) -> bytes:
    payload = {"model": model, "prompt": prompt}
    if size:
        payload["size"] = size
    if quality:
        payload["quality"] = quality
    return _parse_image_response(_post_json(f"{base}/images/generations", key, payload, timeout))


def api_edit(base, key, model, prompt, size, quality, ref_files, timeout,
             field="image[]") -> bytes:
    fields = [("model", model), ("prompt", prompt), ("size", size), ("quality", quality)]
    files = [(field, name, blob) for name, blob in ref_files]
    return _parse_image_response(_post_multipart(f"{base}/images/edits", key, fields,
                                                 files, timeout))


def detect_ext(raw: bytes) -> str:
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if raw[:2] == b"\xff\xd8":
        return ".jpg"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return ".webp"
    return ".png"


def png_dimensions(raw: bytes) -> str:
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", raw[16:24])
        return f"{w}x{h}"
    return "?"


# ---------------------------------------------------------------- 主流程

def load_entries(path: Path) -> tuple[list[dict], dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data if isinstance(data, dict) else {}
    entries = data.get("rows") if isinstance(data, dict) and isinstance(data.get("rows"), list) else data
    if not isinstance(entries, list):
        sys.exit(f"[FAIL] 提示词文件格式不认识（要 rows[] 或 数组）：{path}")
    if meta.get("negative"):
        for e in entries:
            e.setdefault("negative", meta["negative"])
    return entries, meta


# ==================== 出图通道：API 优先 · 工具兜底 ====================
# 规则：本地 API 优先；没 key / 连不通 / 出图失败时不再硬失败，而是写出
#   <出图目录>/generate_image参数.json 并返回退出码 6：
#     · 无参考图的条目 → generate_image(image_configs=[...])，每批 ≤10 张
#     · 有参考图的条目 → edit_image(image_path=<主参考>, prompt=..., size=...)，一次一张
#   工具出图后：python3 scripts/generate_images.py --project <项目> --adopt <图片…>
EXIT_NEED_TOOL = 6
MANIFEST_NAME = "generate_image参数.json"
TOOL_SIZES = ("1024x1024", "1536x1024", "1024x1536", "2048x2048",
              "2048x1152", "3840x2130", "2130x3840")
TOOL_BATCH = 10
IMG_EXTS_ALL = (".png", ".jpg", ".jpeg", ".webp")


def tool_size(size, default="1024x1536"):
    """把任意尺寸映射到 generate_image 的 7 档标准尺寸。"""
    s = str(size or "").strip().lower()
    if s in TOOL_SIZES:
        return s
    try:
        w, h = (int(x) for x in s.split("x"))
    except (ValueError, TypeError):
        return default
    if not w or not h:
        return default
    r = w / h
    big = max(w, h) >= 2000
    if 0.95 <= r <= 1.05:
        return "2048x2048" if big else "1024x1024"
    if r > 1.05:
        if r > 1.9:
            return "3840x2130" if big else "2048x1152"
        return "1536x1024"
    return "1024x1536"


def probe_image_api(base, key, timeout=20):
    """只读探测本地出图 API（免费），返回 (可用?, 说明)。"""
    if not key:
        return False, "没读到 API key（--key / NEWAPI_IMAGE_KEY / config.json newapi_image_key）"
    if not base:
        return False, "没有 base_url"
    url = base + "/models"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", "Bearer " + key)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read(2048)
        return True, f"HTTP 200（{url}）"
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, f"HTTP {e.code}：key 被拒（{url}）"
        if e.code in (404, 405):
            return True, f"HTTP {e.code}：/models 未实现，但网关可达，按可用处理"
        return False, f"HTTP {e.code}（{url}）"
    except Exception as e:  # noqa: BLE001
        return False, f"连不通：{e}"


def build_tool_manifest(items, target_rel, reason, adopt_hint):
    """items: [{id,file,size,tool,prompt,refs,call?}]；generate_image 按 ≤10 张分批。"""
    gen = [it for it in items if it.get("tool") == "generate_image"]
    batches = [[{"prompt": it["prompt"], "size": it["size"], "output_format": "png"}
                for it in gen[i:i + TOOL_BATCH]]
               for i in range(0, len(gen), TOOL_BATCH)]
    return {
        "note": ("本地出图 API 不可用时的兜底清单：无参考图用 generate_image（每批 ≤10 张），"
                 "有参考图用 edit_image（一次一张）。出图后按 items 顺序 --adopt 收位。"),
        "channel": "tool",
        "reason": reason,
        "target_dir": target_rel,
        "generate_count": len(gen),
        "edit_count": len(items) - len(gen),
        "items": items,
        "batches": batches,
        "after": adopt_hint + " <图片…>",
    }


def print_tool_handoff(manifest_path, manifest):
    print("")
    print(f"[降级] 本地出图 API 不可用（{manifest['reason']}）→ 改走宿主工具 generate_image / edit_image")
    print(f"[清单] {manifest_path}")
    print(f"[任务] generate_image {manifest['generate_count']} 张"
          f"（{len(manifest['batches'])} 批）· edit_image {manifest['edit_count']} 张")
    for i, batch in enumerate(manifest["batches"], 1):
        print("-" * 60)
        print(f"[generate_image 第 {i}/{len(manifest['batches'])} 批 · {len(batch)} 张]")
        for j, cfg in enumerate(batch, 1):
            print(f"  {j}) size={cfg['size']}")
            print(f"     {cfg['prompt']}")
    edits = [it for it in manifest["items"] if it.get("tool") == "edit_image"]
    if edits:
        print("-" * 60)
        print(f"[edit_image · {len(edits)} 张，一次一张]")
        for it in edits:
            call = it.get("call") or {}
            print(f"  - {it['id']} → {it['file']}")
            print(f"    edit_image(image_path=\"{call.get('image_path', '')}\", "
                  f"prompt=<见清单>, size=\"{it['size']}\")")
            if call.get("ref_paths"):
                print(f"    （多参考图可选：再加 ref_paths={call['ref_paths']}）")
    print("-" * 60)
    print(f"[收位] {manifest['after']}")


def image_size_bytes(raw):
    """从 PNG / JPEG 头里读宽高（读不出返回 0,0）。"""
    if raw[:8] == b"\x89PNG\r\n\x1a\n" and len(raw) >= 24:
        w, h = struct.unpack(">II", raw[16:24])
        return int(w), int(h)
    if raw[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(raw):
            if raw[i] != 0xFF:
                i += 1
                continue
            marker = raw[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", raw[i + 5:i + 9])
                return int(w), int(h)
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack(">H", raw[i + 2:i + 4])[0]
    return 0, 0


def _write_png(src, dst):
    raw = open(src, "rb").read()
    if not raw:
        raise RuntimeError("空文件")
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        with open(dst, "wb") as f:
            f.write(raw)
        return image_size_bytes(raw)
    ff = shutil.which("ffmpeg")
    if not ff:
        raise RuntimeError("非 PNG 且本机没有 ffmpeg（brew install ffmpeg）")
    subprocess.run([ff, "-y", "-v", "error", "-i", src, "-frames:v", "1", dst], check=True)
    with open(dst, "rb") as f:
        return image_size_bytes(f.read())


def _natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def adopt_tool_images(paths, manifest_path, proj_dir, force=False):
    """按清单顺序收位工具出好的图；支持目录、按序文件、id=路径。"""
    if not os.path.isfile(manifest_path):
        print(f"[FAIL] 找不到出图清单：{manifest_path}\n"
              f"       先跑一次本脚本（API 不通会自动写出），或加 --tool-json 生成")
        return 1
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    items = [it for it in (manifest.get("items") or []) if it.get("id")]
    if not items:
        print("[FAIL] 清单里没有 items")
        return 1
    by_id = {str(it["id"]): it for it in items}
    mapping, plain = {}, []
    for p in paths:
        key = p.split("=", 1)[0] if "=" in p else ""
        if key in by_id:
            mapping[key] = p.split("=", 1)[1]
        else:
            plain.append(p)

    expanded = []
    for p in plain:
        full = p if os.path.isabs(p) else os.path.join(proj_dir, p)
        if os.path.isdir(full):
            expanded.extend(sorted(
                (os.path.join(full, f) for f in os.listdir(full)
                 if f.lower().endswith(IMG_EXTS_ALL)),
                key=lambda x: _natural_key(os.path.basename(x))))
        else:
            expanded.append(full)
    pending = [it for it in items if str(it["id"]) not in mapping]
    if len(expanded) != len(pending):
        print(f"[FAIL] 图片数与清单不符：给了 {len(expanded)} 张，清单待收位 {len(pending)} 张")
        print("       待收位：" + "、".join(str(it["id"]) for it in pending[:20])
              + ("…" if len(pending) > 20 else ""))
        print("       可改用 id=路径 精确对应，或 --adopt <目录>（按文件名自然排序）")
        return 1
    for it, path in zip(pending, expanded):
        mapping[str(it["id"])] = path

    done = 0
    skipped = 0
    for it in items:
        eid = str(it["id"])
        src = mapping.get(eid)
        if not src:
            continue
        if not os.path.isfile(src):
            print(f"[FAIL] {eid} 图片不存在：{src}")
            continue
        target = it["file"] if os.path.isabs(it["file"]) else os.path.join(proj_dir, it["file"])
        os.makedirs(os.path.dirname(target) or proj_dir, exist_ok=True)
        if os.path.isfile(target) and not force:
            print(f"[skip] {eid}（已存在；覆盖加 --force）")
            skipped += 1
            continue
        try:
            w, h = _write_png(src, target)
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {eid} 收位失败：{e}")
            continue
        done += 1
        print(f"[完成] {eid} → {it['file']}（{w}x{h}，{os.path.getsize(target) // 1024} KB）")
    tail = f"（另有 {skipped} 张已存在跳过）" if skipped else ""
    print(f"\n[收位] {done}/{len(mapping)} 张已就位{tail}")
    print("[下一步] 先看这些图：主体对不对、风格对不对、有没有文字。不对就改提示词重出。")
    return 0 if done + skipped == len(mapping) else 1


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser(description="MV 参考图批量出图（读 文生图提示词.json）")
    ap.add_argument("--project", required=True, help="项目目录，或 assets/output 下的项目名")
    ap.add_argument("--prompts", default=DEFAULT_PROMPTS, help=f"提示词文件（默认 {DEFAULT_PROMPTS}）")
    ap.add_argument("--img-dir", default=IMAGE_ROOT, help=f"图片根目录名（默认 {IMAGE_ROOT}）")
    ap.add_argument("--kind", default="", help="只出某风格（按 kind 字段）")
    ap.add_argument("--id", default="", help="只出指定 id（前缀匹配，逗号分隔）")
    ap.add_argument("--size", default="", help="统一覆盖尺寸（如 1536x1152）")
    ap.add_argument("--ratio", default="", choices=["", *RATIO_TO_SIZE.keys()],
                    help="按取向统一覆盖尺寸（4:3→1536x1152，16:9→1536x1024，9:16→1024x1536，3:4→1152x1536）")
    ap.add_argument("--base-url", default="")
    ap.add_argument("--key", default="")
    ap.add_argument("--model", default="")
    ap.add_argument("--quality", default="", help="quality（默认取 config；传 none 则不带该参数）")
    ap.add_argument("--ref-field", default="image[]", help="多图 multipart 字段名（默认 image[]）")
    ap.add_argument("--limit", type=int, default=0, help="最多出几张（0=不限）")
    ap.add_argument("--force", action="store_true", help="已存在的图也重新生成")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不调接口")
    ap.add_argument("--yes", action="store_true", help="★确认真的调用付费接口出图")
    ap.add_argument("--all", action="store_true", help="串行连出全部待出图（默认只出 1 张）")
    ap.add_argument("--batch", action="store_true", help="并发出图（需配 --concurrency；默认关闭）")
    ap.add_argument("--concurrency", type=int, default=3, help="--batch 的并发数（默认 3）")
    ap.add_argument("--timeout", type=int, default=180, help="单张超时秒数（默认 180）")
    ap.add_argument("--retries", type=int, default=1, help="失败重试次数（默认 1）")
    ap.add_argument("--probe", action="store_true",
                    help="只探测本地出图 API（免费）：0=可用 / 6=需走 generate_image")
    ap.add_argument("--tool-json", action="store_true",
                    help=f"不出图，只写 {MANIFEST_NAME}（generate_image / edit_image 参数）")
    ap.add_argument("--adopt", nargs="*", default=[],
                    help="工具出图后收位：按清单顺序给图片/目录，或 id=路径")
    ap.add_argument("--no-fallback", "--api-only", dest="no_fallback", action="store_true",
                    help="API 失败不降级到工具，直接退出 1（默认降级并退出 6）")
    args = ap.parse_args()

    project = resolve_project(args.project)
    cfg = image_api_config()
    base = normalize_base(args.base_url or cfg["base_url"])
    key = args.key or cfg["key"]
    model = args.model or cfg["model"]
    quality = "" if (args.quality or "").lower() == "none" else (args.quality or cfg["quality"])
    size_override = args.size or RATIO_TO_SIZE.get(args.ratio, "")

    # ① 只探通道：不读提示词、不花钱
    if args.probe:
        ok, detail = probe_image_api(base, key, min(args.timeout, 30))
        print(f"[通道] {'A 本地 API 可用' if ok else 'B 走 generate_image / edit_image（API 不可用）'}：{detail}")
        return 0 if ok else EXIT_NEED_TOOL


    img_root = project / args.img_dir
    manifest_path = img_root / MANIFEST_NAME
    adopt_hint = f"python3 scripts/generate_images.py --project {args.project} --img-dir {args.img_dir} --adopt"

    # ② 工具出图后收位：只读清单，不读提示词
    if args.adopt or "--adopt" in sys.argv[1:]:
        if not args.adopt:
            print("[FAIL] --adopt 后面要跟图片/目录，或 id=路径")
            print(f"       例：{adopt_hint} {args.img_dir}/")
            return 2
        return adopt_tool_images(args.adopt, str(manifest_path), str(project), force=args.force)

    # ③ 以下（预览 / 出图）才需要提示词文件
    prompts_path = Path(args.prompts).expanduser()
    if not prompts_path.is_absolute():
        prompts_path = project / prompts_path
    if not prompts_path.is_file():
        sys.exit(f"[FAIL] 找不到提示词文件：{prompts_path}")
    entries, meta = load_entries(prompts_path)

    if args.kind:
        entries = [e for e in entries if (e.get("kind") or "") == args.kind]
    if args.id:
        pats = [p.strip() for p in args.id.split(",") if p.strip()]
        entries = [e for e in entries if any(str(e.get("id", "")).startswith(p) for p in pats)]


    def kind_dir(kind: str) -> Path:
        k = (kind or "").strip()
        return img_root / k if k else img_root

    def make_items(rows_):
        items = []
        for e in rows_:
            eid = str(e["id"])
            size = tool_size(size_override or e.get("size") or "")
            refs = e.get("refs") or []
            if isinstance(refs, str):
                refs = [refs]
            ref_paths = []
            for ref in refs:
                hit = find_ref_image(project, str(ref))
                if hit:
                    ref_paths.append(str(hit.relative_to(project)))
            prompt = str(e["prompt"])
            item = {
                "id": eid,
                "file": str((kind_dir(str(e.get("kind") or "")) / (eid + ".png")).relative_to(project)),
                "size": size,
                "tool": "edit_image" if ref_paths else "generate_image",
                "prompt": prompt,
            }
            if ref_paths:
                item["refs"] = ref_paths
                item["call"] = {"tool": "edit_image", "image_path": ref_paths[0],
                                "ref_paths": ref_paths[1:], "prompt": prompt, "size": size}
            items.append(item)
        return items

    def handoff(reason, rows_):
        """API 走不通：写出工具清单并交棒（退出码 6）。"""
        if args.no_fallback:
            print(f"[FAIL] 出图 API 不可用（{reason}）；--no-fallback 已关闭降级")
            return 1
        items = make_items(rows_)
        if not items:
            print("[完成] 没有需要出的图。")
            return 0
        manifest = build_tool_manifest(items, args.img_dir, reason, adopt_hint)
        img_root.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print_tool_handoff(str(manifest_path), manifest)
        return EXIT_NEED_TOOL

    def existing(eid: str) -> Path | None:
        if not img_root.is_dir():
            return None
        for ext in IMG_EXTS:
            hit = next(img_root.rglob(eid + ext), None)
            if hit and hit.is_file():
                return hit
        return None

    todo = [e for e in entries if e.get("id") and e.get("prompt")
            and (args.force or not existing(str(e["id"])))]
    for e in entries:
        if e.get("id") and e.get("prompt") and not args.force and existing(str(e["id"])):
            print(f"[skip] {e['id']}（已存在）")
    if args.limit:
        todo = todo[:args.limit]

    key_desc = f"{key[:8]}…{key[-4:]}" if key else "(未提供)"
    print(f"[项目] {project}")
    print(f"[配置] base={base}  model={model}  quality={quality or '(默认)'}  key={key_desc}")
    print(f"[计划] 待出 {len(todo)} 张 → {img_root}/<kind>/")

    if args.dry_run:
        for e in todo:
            print(f"  - [{e.get('kind')}] {e['id']}  size={size_override or e.get('size') or '(默认)'}"
                  f"  refs={e.get('refs') or '无'}")
        print("[dry-run] 未调接口。")
        return 0
    if args.tool_json:
        print("[通道] B 指定：只写 generate_image / edit_image 参数，不调本地 API")
        return handoff("--tool-json 指定走工具通道", todo)
    if not todo:
        print("[完成] 无待出图。")
        return 0
    if not key:
        return handoff("没读到 API key", todo)

    # ── 成本闸门：默认一张一张；连出必须显式 --all / --batch ──
    if not (args.all or args.batch) and len(todo) > 1:
        print(f"[一张一张出] 本次只出 1 张，还有 {len(todo)} 张待出。")
        print(f"             本次出：{todo[0]['id']}")
        print("             出完核对再跑一次即出下一张（已存在的自动跳过）；要连出加 --all。")
        todo = todo[:1]
    if not args.yes:
        print(f"\n[STOP] 未加 --yes，已中止：本次将调用**付费接口**出 {len(todo)} 张图。")
        print("       确认出图：加 --yes　　只看清单：加 --dry-run　　更省：--quality medium --size 1024x1024")
        return 0

    workers = max(1, args.concurrency) if args.batch else 1
    if args.batch and args.concurrency > 8:
        print("[warn] 并发 >8 容易被网关限流，已按 8 跑。", file=sys.stderr)
        workers = 8
    lock = threading.Lock()

    def gen_one(idx: int, entry: dict):
        eid = str(entry["id"])
        size = size_override or entry.get("size") or ""
        refs = entry.get("refs") or []
        if isinstance(refs, str):
            refs = [refs]
        ref_files = []
        for ref in refs:
            path = find_ref_image(project, str(ref))
            if path:
                ref_files.append((path.name, path.read_bytes()))
            else:
                with lock:
                    print(f"[{idx}/{len(todo)}] ⚠ {eid} 参考图缺失({ref})，本次降级为纯文生图", flush=True)
        t0, raw, err = time.time(), None, None
        for attempt in range(args.retries + 1):
            with lock:
                tag = f"（第 {attempt + 1}/{args.retries + 1} 次尝试）" if args.retries else ""
                print(f"[{idx}/{len(todo)}] → 请求已发出{tag}，等待中（超时 {args.timeout}s）…", flush=True)
            try:
                if ref_files:
                    raw = api_edit(base, key, model, entry["prompt"], size, quality,
                                   ref_files, args.timeout, field=args.ref_field)
                else:
                    raw = api_generate(base, key, model, entry["prompt"], size, quality, args.timeout)
                break
            except RuntimeError as exc:
                err = str(exc)
                if attempt < args.retries:
                    with lock:
                        print(f"[{idx}/{len(todo)}] {eid} 重试({attempt + 1}/{args.retries})…", flush=True)
                    time.sleep(5 * (attempt + 1))
        if raw is None:
            with lock:
                print(f"[{idx}/{len(todo)}] ✗ {eid} · {err}", flush=True)
            return eid, None, err
        out_dir = kind_dir(str(entry.get("kind") or ""))
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / (eid + detect_ext(raw))
        out.write_bytes(raw)
        with lock:
            print(f"[{idx}/{len(todo)}] ✓ {eid} · {time.time() - t0:.0f}s · "
                  f"{len(raw) // 1024}KB · {png_dimensions(raw)} → {out.relative_to(project)}", flush=True)
        return eid, out, None

    ok, fail = 0, []
    t_all = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(gen_one, i, e) for i, e in enumerate(todo, 1)]
        for fut in concurrent.futures.as_completed(futures):
            eid, _path, err = fut.result()
            if err is None:
                ok += 1
            else:
                fail.append((eid, err))

    print(f"\n[完成] 成功 {ok} / {len(todo)}（并发 {workers}），总耗时 {(time.time() - t_all) / 60:.1f} 分钟")
    if fail:
        print("[失败清单]")
        for eid, err in fail:
            print(f"  - {eid}: {err[:160]}")
        fail_ids = {eid for eid, _err in fail}
        rows_bad = [e for e in todo if str(e["id"]) in fail_ids]
        print("[说明] 失败的那几张已写进工具清单：可以修 API 后 --force 重出，也可以走 generate_image")
        return handoff("API 出图失败：" + str(fail[0][1]).splitlines()[0][:80], rows_bad)
    print(f"[下一步] 核对图片后跑：python3 scripts/upload_project.py {project} --verify --fill-json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
