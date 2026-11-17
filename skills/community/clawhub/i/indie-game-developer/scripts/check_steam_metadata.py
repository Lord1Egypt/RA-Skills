#!/usr/bin/env python3
"""Steam 商店元数据校验 —— 校验商店页元数据 JSON 是否字段齐备、合规。

纯标准库（argparse / json），不联网、不修改被检文件，产出确定可复现。
配合 assets/steam-store-metadata-template.json（含 _ 注释键，脚本自动跳过）使用。

检测项：
  E1  必填字段缺失或为空：name / short_description / about_the_game / header_image
  E2  列表字段过短：screenshots < 3（Steam 强要求），tags < 5（发现流量不足）
  E3  capsules / genres / supported_languages / release_date / pricing 缺失（影响上架/发现）
  W1  tags > 20（超出 Steam 推荐上限）
  W2  short_description 过短(<80)或过长短描述字段

用法:
  python3 scripts/check_steam_metadata.py --metadata assets/steam-store-metadata-template.json
  python3 scripts/check_steam_metadata.py --metadata my-metadata.json --json
"""
from __future__ import annotations

import argparse
import json
import sys

REQUIRED_NONEMPTY = ["name", "short_description", "about_the_game", "header_image"]
REQUIRED_LIST_MIN = {"screenshots": 3, "tags": 5}
REQUIRED_PRESENT = ["capsules", "genres", "supported_languages", "release_date", "pricing"]


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    # 跳过 _ 开头的注释键，不当成字段
    return {k: v for k, v in data.items() if not str(k).startswith("_")}


def main() -> int:
    ap = argparse.ArgumentParser(description="校验 Steam 商店元数据 JSON（纯标准库）")
    ap.add_argument("--metadata", required=True, help="商店元数据 JSON")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    try:
        data = load(args.metadata)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  [✗] 解析失败: {e}")
        return 1

    findings = []

    for f in REQUIRED_NONEMPTY:
        val = data.get(f)
        if not val or not str(val).strip():
            findings.append({"severity": "error", "check": "必填字段",
                             "detail": f"{f} 缺失或为空"})

    for f, mn in REQUIRED_LIST_MIN.items():
        val = data.get(f)
        if not isinstance(val, list) or len(val) < mn:
            got = len(val) if isinstance(val, list) else 0
            findings.append({"severity": "error", "check": "列表字段",
                             "detail": f"{f} 数量 {got} < 最少 {mn}"})

    for f in REQUIRED_PRESENT:
        if f not in data or data.get(f) in (None, "", [], {}):
            findings.append({"severity": "error", "check": "必填字段",
                             "detail": f"{f} 缺失或为空（影响上架/发现）"})

    tags = data.get("tags")
    if isinstance(tags, list) and len(tags) > 20:
        findings.append({"severity": "warn", "check": "标签数",
                         "detail": f"tags {len(tags)} > 20，超出 Steam 推荐上限"})

    sd = data.get("short_description")
    if isinstance(sd, str):
        if len(sd) < 80:
            findings.append({"severity": "warn", "check": "短描述",
                             "detail": f"short_description 仅 {len(sd)} 字符，建议 ≥80"})
        elif len(sd) > 200:
            findings.append({"severity": "warn", "check": "短描述",
                             "detail": f"short_description {len(sd)} 字符，Steam 列表仅显示前若干"})

    errors = [f for f in findings if f["severity"] == "error"]
    if args.json:
        print(json.dumps({"errors": len(errors), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        for f in findings:
            mark = "✗" if f["severity"] == "error" else "!"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        print(f"\n结果：{len(errors)} error, {len(findings) - len(errors)} warning")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
