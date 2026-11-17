#!/usr/bin/env python3
"""游戏资源引用完整性检查 —— 扫描源码中对资源文件(贴图/模型/音频/字体/精灵表)的
引用，校验被引用的文件是否真实存在，防止"运行时缺图/裂图"这类最痛的 bug。

纯标准库（argparse / json / re / os），不联网、不修改被检文件，产出确定可复现。
两种模式：
  扫描模式  --scan DIR...            在源码目录里抽取字符串字面量中的资源路径并校验存在
  清单模式  --manifest FILE --root D 校验 JSON 清单里列出的资源路径都存在（清单含 _ 注释键，自动跳过）
配合 references/asset-pipeline.md 使用。

检测项：
  E1  扫描/清单中引用的资源文件不存在（路径相对源文件目录或 --root 均找不到）
  W1  扫描命中疑似资源字符串但无法判定（仅提示，不阻断）

用法:
  python3 scripts/check_asset_refs.py --scan src/ --root .
  python3 scripts/check_asset_refs.py --manifest assets/asset-manifest-example.json --root .
  python3 scripts/check_asset_refs.py --scan src/ --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ASSET_EXT = {
    "png", "jpg", "jpeg", "gif", "webp", "svg", "bmp",
    "glb", "gltf", "obj", "fbx",
    "mp3", "wav", "ogg", "flac",
    "ttf", "otf", "woff", "woff2",
    "atlas", "json",
}
SKIP_DIRS = {".git", "node_modules", "build", "dist", ".dart_tool", "Pods"}
# 抽取单/双/反引号内的资源路径（按扩展名过滤）
REF_RE = re.compile(r"""['"`]([^'"`\n]+\.(?:%s))['"`]""" % "|".join(ASSET_EXT))


def iter_text_files(root: str):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.endswith((".md", ".py", ".js", ".ts", ".tsx", ".jsx",
                            ".json", ".html", ".css", ".gd", ".cs", ".lua")):
                yield os.path.join(dirpath, fn)


def resolve(ref: str, base_dir: str, root: str) -> bool:
    cands = [os.path.normpath(os.path.join(base_dir, ref)),
             os.path.normpath(os.path.join(root, ref))]
    return any(os.path.isfile(c) for c in cands)


def scan_dirs(dirs, root: str):
    findings = []
    for d in dirs:
        for path in iter_text_files(d):
            base = os.path.dirname(path)
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            for m in REF_RE.finditer(text):
                ref = m.group(1)
                if not resolve(ref, base, root):
                    findings.append({
                        "severity": "error", "check": "资源缺失",
                        "detail": f"{path}: 引用 {ref} 但文件不存在",
                    })
    return findings


def check_manifest(manifest: str, root: str):
    findings = []
    with open(manifest, encoding="utf-8") as fh:
        data = json.load(fh)
    # 跳过 _ 开头的注释键
    items = data.get("assets") if isinstance(data, dict) else data
    if not isinstance(items, list):
        return [{"severity": "error", "check": "清单格式",
                 "detail": f"{manifest}: 缺少 assets 列表或顶层非数组"}]
    for ref in items:
        if str(ref).startswith("_"):
            continue
        if not resolve(str(ref), root, root):
            findings.append({
                "severity": "error", "check": "资源缺失",
                "detail": f"{manifest}: 资源 {ref} 不存在",
            })
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="校验游戏资源引用完整性（纯标准库）")
    ap.add_argument("--scan", nargs="*", default=[], help="扫描的源码目录")
    ap.add_argument("--manifest", help="资源清单 JSON（含 _ 注释键，自动跳过）")
    ap.add_argument("--root", default=".", help="解析相对路径的根目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not args.scan and not args.manifest:
        ap.error("至少需要 --scan 或 --manifest 之一")

    findings = []
    if args.scan:
        findings += scan_dirs(args.scan, args.root)
    if args.manifest:
        findings += check_manifest(args.manifest, args.root)

    errors = [f for f in findings if f["severity"] == "error"]
    if args.json:
        print(json.dumps({"errors": len(errors), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        for f in findings:
            mark = "✗" if f["severity"] == "error" else "!"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        print(f"\n结果：{len(errors)} error")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
