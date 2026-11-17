#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_integrity_manifest.py — 生成 data/INTEGRITY_MANIFEST.json（v7.6.0）。

data/ 与 references/ 全部 JSON 的 SHA256+字节数清单。文件内容变更后必须重跑本工具，
否则 pp_doctor --deep 判 FAIL（完整性自证的单一事实源）。"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _build():
    """构造清单（v7.7.0 单一来源化：generated 版本读 skill.json，禁硬编码）。"""
    files = sorted(
        [f"data/{p.name}" for p in (ROOT / "data").glob("*.json")
         if p.name != "INTEGRITY_MANIFEST.json"] +
        [f"references/{p.name}" for p in (ROOT / "references").glob("*.json")]
    )
    try:
        ver = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))["version"]
    except Exception:
        ver = "unknown"
    manifest = {"_meta": "安装完整性清单：data/ 与 references/ 全部 JSON 的 SHA256 与字节数。"
                         "pp_doctor --deep 逐文件核对（哈希+解析双重验证）；发布链打包后对打包副本再核对一次。"
                         "由 eval/gen_integrity_manifest.py 生成（单一来源；generated 随 skill.json 版本）。",
                "generated": ver,
                "files": {}}
    for rel in files:
        b = (ROOT / rel).read_bytes()
        manifest["files"][rel] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return manifest


def main():
    import argparse
    ap = argparse.ArgumentParser(description="生成/校验 INTEGRITY_MANIFEST.json")
    ap.add_argument("--check", action="store_true",
                    help="校验模式：不落盘，只验证现有清单与重新生成的输出逐字节一致（发布闸用）")
    a = ap.parse_args()
    manifest = _build()
    rendered = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out = ROOT / "data" / "INTEGRITY_MANIFEST.json"
    if a.check:
        current = out.read_text(encoding="utf-8") if out.is_file() else ""
        if current == rendered:
            print(f"check OK: {len(manifest['files'])} files, manifest 与生成器输出逐字节一致")
            return 0
        print("check FAIL: 随包清单与生成器输出不一致——数据文件变更后未重跑生成器？", file=sys.stderr)
        return 1
    out.write_text(rendered, encoding="utf-8")
    print(f"manifest: {len(manifest['files'])} files -> {out} (generated={manifest['generated']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
