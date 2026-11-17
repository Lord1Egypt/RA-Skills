#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_assets.py · 把 ⑤ 产物里的素材引用统一换成「完整直链」

为什么需要：
  - 「@图1_人物参考.png」只是本地文件名，出片平台/网关并不能凭它去取图；
  - 分镜JSON 的 refs_urls 也常常还是本地相对路径；
  - 于是投递时要么 404，要么必须靠平台自己按序上传，非常容易错位。

这个脚本做三件事（不改提示词文字，只把「素材指向」补全）：
  1) 分镜JSON.json：refs_urls → 绝对直链（默认百分号编码）
  2) 裸请求体/*.json：content 里的 image_url / audio_url → 绝对直链
  3) 提示词.md：在 `@图N_名称.png` 后面补上「（https://…）」完整链接

用法：
  python3 scripts/link_assets.py "<项目>" --dry-run
  python3 scripts/link_assets.py "<项目>" --verify
  python3 scripts/link_assets.py "<项目>" --base https://your-static-host.example.com/public/mv --namespace MV01-xxx
  python3 scripts/link_assets.py "<项目>" --revert      # 退回本地相对路径（离线出片走 base64 时用）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG = SKILL_ROOT / "scripts" / "config.json"
PLAN_DIRS = ("04-提示词",)
PLAN_NAME = "分镜JSON.json"
IMAGE_ROOT = "04-图片"
AUDIO_ROOT = "00-输入"


def _encode_rel(rel: str) -> str:
    """逐段百分号编码（中文/空格），保留 /；已含 %XX 的段不二次编码。"""
    out = []
    for seg in rel.split("/"):
        parts = seg.split("%")
        already = len(parts) > 1 and all(len(p) == 2 or p == "" for p in parts[1:]) and not any(ord(c) > 127 for c in seg)
        out.append(seg if already else quote(seg, safe="-_.~"))
    return "/".join(out)


def _rel_from(value: str) -> str | None:
    """把 URL/路径还原成项目内的相对路径（如 图片/<kind>/图1.png）。"""
    text = str(value or "").strip()
    if not text or text.startswith("data:"):
        return None
    path = unquote(urlparse(text).path) if "://" in text else text
    idx = path.find(IMAGE_ROOT)
    if idx < 0:
        idx = path.find(AUDIO_ROOT)
    return path[idx:] if idx >= 0 else None


def build(value: str, base: str, ns: str, revert: bool, encode: bool) -> str:
    rel = _rel_from(value)
    prefix = f"{base.rstrip('/')}/{ns.strip('/')}/"
    if revert:
        return rel if rel else value
    if rel is None:
        return value if str(value).startswith(("http://", "https://", "data:")) else value
    return prefix + (_encode_rel(rel) if encode else rel)


def main() -> int:
    ap = argparse.ArgumentParser(description="把 04-提示词 产物里的素材引用换成完整直链")
    ap.add_argument("project", help="项目目录，或 assets/output 下的项目名")
    ap.add_argument("--base", default="", help="外链根（默认读 scripts/config.json 的 asset_url_base）")
    ap.add_argument("--namespace", default="", help="命名空间（默认取项目文件夹名）")
    ap.add_argument("--plan-dir", default=PLAN_DIRS[0], help=f"提示词产物目录（默认 {PLAN_DIRS[0]}）")
    ap.add_argument("--md", dest="md", action="store_true", default=True, help="同时补全 S*.md（默认开）")
    ap.add_argument("--no-md", dest="md", action="store_false", help="不动 md，只改 JSON")
    ap.add_argument("--no-encode", action="store_true", help="不做百分号编码（默认开）")
    ap.add_argument("--revert", action="store_true", help="退回本地相对路径")
    ap.add_argument("--verify", action="store_true", help="改写后逐条 HEAD 核验（需网络）")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不写盘")
    args = ap.parse_args()

    project = Path(args.project).expanduser()
    if not project.is_dir():
        cand = SKILL_ROOT / "assets" / "output" / args.project
        if cand.is_dir():
            project = cand
        else:
            sys.exit(f"[FAIL] 项目目录不存在：{args.project}")
    project = project.resolve()

    base = args.base
    if not base:
        try:
            base = json.loads(CONFIG.read_text(encoding="utf-8")).get("asset_url_base", "")
        except Exception:  # noqa: BLE001
            base = ""
    if not base:
        sys.exit("[FAIL] 没给 --base，config.json 里也没有 asset_url_base")
    ns = args.namespace.strip("/") or project.name
    encode = not args.no_encode

    plan_dir = project / args.plan_dir
    json_path = plan_dir / PLAN_NAME
    if not json_path.is_file():
        sys.exit(f"[FAIL] 找不到 {json_path}")

    doc = json.loads(json_path.read_text(encoding="utf-8"))
    changed = 0
    for shot in doc.get("shots", []):
        for key in ("refs_urls", "ref_audio_urls"):
            vals = shot.get(key)
            if not vals:
                continue
            new = []
            for v in vals:
                nv = build(str(v), base, ns, args.revert, encode)
                if nv != v:
                    changed += 1
                new.append(nv)
            shot[key] = new

    # 裸请求体
    bodies = sorted((plan_dir / "裸请求体").glob("*.json"))
    body_changed = 0
    for f in bodies:
        b = json.loads(f.read_text(encoding="utf-8"))
        for c in b.get("content", []):
            for key in ("image_url", "audio_url", "video_url"):
                node = c.get(key)
                if isinstance(node, dict) and node.get("url"):
                    nv = build(node["url"], base, ns, args.revert, encode)
                    if nv != node["url"]:
                        node["url"] = nv
                        body_changed += 1

    # md：给 @图N_名称.png 补「（完整链接）」
    md_changed = 0
    md_files = sorted(plan_dir.glob("S*.md")) if args.md else []
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        def repl(m: re.Match) -> str:
            token = m.group(0)
            if text[m.end():m.end() + 6].startswith("（http"):
                return token
            name = token.lstrip("@")
            rel = None
            for shot in doc.get("shots", []):
                for u in shot.get("refs_urls", []):
                    if Path(unquote(urlparse(u).path if "://" in u else u)).name == name:
                        rel = _rel_from(u)
                        break
                if rel:
                    break
            if not rel:
                return token
            url = base.rstrip("/") + "/" + ns + "/" + (_encode_rel(rel) if encode else rel)
            return f"{token}（{url}）"
        new_text, n = re.subn(r"@图[0-9A-Za-z_\-\.\u4e00-\u9fff]+\.png", repl, text)
        # 清理重复追加：把紧跟同一个 url 的重复括号块合并
        new_text = re.sub(r"（(https?://[^）]+)）(（\1）)+", r"（\1）", new_text)
        if new_text != text:
            md_changed += 1
            if not args.dry_run:
                f.write_text(new_text, encoding="utf-8")

    if args.dry_run:
        sample = doc["shots"][0]
        print("[dry-run] 例：", sample.get("refs_urls", [])[:1], (sample.get("ref_audio_urls") or [])[:1])
        print(f"[dry-run] 将改 JSON {changed} 处 · 裸请求体 {body_changed} 处 · md {md_changed} 个（未写盘，编码={'开' if encode else '关'}）")
        return 0

    json_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    for f in bodies:
        b = json.loads(f.read_text(encoding="utf-8"))
        for c in b.get("content", []):
            for key in ("image_url", "audio_url", "video_url"):
                node = c.get(key)
                if isinstance(node, dict) and node.get("url"):
                    node["url"] = build(node["url"], base, ns, args.revert, encode)
        f.write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"[完成] JSON {changed} 处 · 裸请求体 {body_changed} 处 · md {md_changed} 个"
          f"（编码={'开' if encode else '关'} · 命名空间={ns}）")

    if args.verify:
        import urllib.request
        urls = set()
        for shot in doc.get("shots", []):
            urls.update(shot.get("refs_urls") or [])
            urls.update(shot.get("ref_audio_urls") or [])
        bad = 0
        for u in sorted(urls):
            try:
                req = urllib.request.Request(u, method="HEAD")
                with urllib.request.urlopen(req, timeout=15) as resp:
                    code = resp.status
            except Exception as exc:  # noqa: BLE001
                code = f"ERR:{exc.__class__.__name__}"
            if code != 200:
                bad += 1
                print(f"  ❌ [{code}] {u}")
        print(f"[verify] ❌ {bad} / {len(urls)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
