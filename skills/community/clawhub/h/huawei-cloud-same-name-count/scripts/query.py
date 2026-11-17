#!/usr/bin/env python3
"""Query same-name population counts (同名人数) from a built-in sample dataset.

Given a name (``--name``), this tool returns how many people share it in the
bundled sample dataset (``scripts/data.json``). The result can be narrowed with
``--gender`` and/or ``--province``, in which case the total and the per-dimension
breakdown only cover the matching records. When nothing matches, an explicit
message is printed — the query never fails silently.

The dataset is **sample/demo data** (a reproducible offline fixture), not an
authoritative population register; it ships with the skill and can be replaced
with ``--data``.

This module is pure Python 3 standard library. It does not call the Huawei Cloud
CLI, any Huawei Cloud SDK, or any REST API, and it touches no cloud resource.

Public API:
    load_data(path=None) -> dict
    normalize_gender(value, genders) -> str
    normalize_province(value, provinces) -> str
    query(name, gender=None, province=None, data=None) -> dict
    render_markdown(result) -> str
    render_text(result) -> str
    render_json(result) -> str
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Sequence

DEFAULT_GENDERS: Sequence[str] = ("男", "女")

# Accept both the canonical Chinese label and common ASCII aliases.
GENDER_ALIASES: Dict[str, str] = {
    "男": "男", "male": "男", "m": "男", "man": "男", "男性": "男",
    "女": "女", "female": "女", "f": "女", "woman": "女", "女性": "女",
}

# Common province aliases -> canonical dataset label. Trailing 省/市 is stripped
# before lookup; entries here cover the short forms people actually type.
PROVINCE_ALIASES: Dict[str, str] = {
    "北京市": "北京", "上海": "上海", "上海市": "上海",
    "广东省": "广东", "浙江省": "浙江", "江苏省": "江苏",
    "山东省": "山东", "河南省": "河南", "四川省": "四川",
}


def _default_data_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def load_data(path: Optional[str] = None) -> Dict[str, object]:
    """Load the dataset as ``{"genders", "provinces", "records", "meta"}``.

    ``records`` is a list of ``{"name", "gender", "province", "count"}`` where
    ``count`` is a non-negative int. Raises ``OSError`` / ``ValueError`` on
    unusable input.
    """
    path = path or _default_data_path()
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("dataset must be a JSON object")
    raw = data.get("records")
    if not isinstance(raw, list) or not raw:
        raise ValueError("dataset must contain a non-empty 'records' array")
    records: List[Dict[str, object]] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name", "")).strip()
        if not name:
            continue
        gender = str(entry.get("gender", "")).strip()
        province = str(entry.get("province", "")).strip()
        try:
            count = int(entry.get("count", 0))
        except (TypeError, ValueError):
            raise ValueError("record count for %r must be an integer" % name)
        if count < 0:
            raise ValueError("record count for %r must be non-negative" % name)
        records.append({"name": name, "gender": gender, "province": province, "count": count})
    if not records:
        raise ValueError("dataset contains no usable records")
    genders = data.get("genders")
    provinces = data.get("provinces")
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    return {
        "genders": list(genders) if isinstance(genders, list) and genders else list(DEFAULT_GENDERS),
        "provinces": list(provinces) if isinstance(provinces, list) else [],
        "records": records,
        "meta": meta,
    }


def normalize_gender(value: str, genders: Sequence[str]) -> str:
    """Map a gender label / alias to a canonical gender, else raise ValueError."""
    key = str(value).strip()
    canonical = GENDER_ALIASES.get(key) or GENDER_ALIASES.get(key.lower())
    if canonical and canonical in genders:
        return canonical
    if key in genders:
        return key
    raise ValueError("unknown gender %r (choose one of: %s)" % (value, ", ".join(genders)))


def normalize_province(value: str, provinces: Sequence[str]) -> str:
    """Map a province label / alias to a canonical province, else raise ValueError."""
    key = str(value).strip()
    for candidate in (key, key.lower()):
        if candidate in PROVINCE_ALIASES and PROVINCE_ALIASES[candidate] in provinces:
            return PROVINCE_ALIASES[candidate]
    stripped = key
    for suffix in ("省", "市"):
        if stripped.endswith(suffix):
            stripped = stripped[: -len(suffix)]
    if stripped in provinces:
        return stripped
    if key in provinces:
        return key
    raise ValueError("unknown province %r (choose one of: %s)" % (value, ", ".join(provinces)))


def _ordered_breakdown(pairs: Dict[str, int], order: Sequence[str]) -> Dict[str, int]:
    """Return the breakdown in canonical order (only non-zero entries)."""
    result: Dict[str, int] = {}
    for key in order:
        if pairs.get(key):
            result[key] = pairs[key]
    for key in sorted(pairs):
        if key not in result and pairs[key]:
            result[key] = pairs[key]
    return result


def query(
    name: str,
    gender: Optional[str] = None,
    province: Optional[str] = None,
    data: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    """Return the same-name count for ``name``, optionally narrowed by filters.

    Result keys: ``name``, ``found`` (the name exists in the dataset at all),
    ``matched`` (at least one record matches name + filters), ``total``,
    ``filters``, ``by_gender``, ``by_province``, ``available_genders``,
    ``available_provinces``, ``records`` and ``message`` (an explicit no-result
    message; empty when a match was found).
    """
    data = data if data is not None else load_data()
    genders: Sequence[str] = data["genders"]  # type: ignore[assignment]
    provinces: Sequence[str] = data["provinces"]  # type: ignore[assignment]
    records: List[Dict[str, object]] = data["records"]  # type: ignore[assignment]

    name = str(name).strip()
    if not name:
        raise ValueError("name must be a non-empty string")

    norm_gender = normalize_gender(gender, genders) if gender is not None else None
    norm_province = normalize_province(province, provinces) if province is not None else None

    name_records = [r for r in records if r["name"] == name]
    found = bool(name_records)

    matched = [
        r for r in name_records
        if (norm_gender is None or r["gender"] == norm_gender)
        and (norm_province is None or r["province"] == norm_province)
    ]
    total = sum(int(r["count"]) for r in matched)

    by_gender: Dict[str, int] = {}
    by_province: Dict[str, int] = {}
    for r in matched:
        by_gender[str(r["gender"])] = by_gender.get(str(r["gender"]), 0) + int(r["count"])
        by_province[str(r["province"])] = by_province.get(str(r["province"]), 0) + int(r["count"])

    available_genders = sorted({str(r["gender"]) for r in name_records})
    available_provinces = sorted({str(r["province"]) for r in name_records})

    message = ""
    if not found:
        message = (
            "未找到姓名「%s」的同名记录：数据集中没有该姓名。"
            "请确认姓名是否正确，或更换数据源（--data）。" % name
        )
    elif not matched:
        filters = []
        if norm_gender is not None:
            filters.append("性别=%s" % norm_gender)
        if norm_province is not None:
            filters.append("省份=%s" % norm_province)
        message = (
            "未找到满足条件的记录：姓名「%s」在数据集中存在，但没有 %s 的数据。"
            "该姓名在数据集中的维度：性别=%s；省份=%s。"
            % (
                name,
                "、".join(filters) or "(无条件)",
                "/".join(available_genders) or "-",
                "/".join(available_provinces) or "-",
            )
        )

    result: Dict[str, object] = {
        "name": name,
        "found": found,
        "matched": bool(matched),
        "total": total,
        "filters": {"gender": norm_gender, "province": norm_province},
        "by_gender": _ordered_breakdown(by_gender, genders),
        "by_province": _ordered_breakdown(by_province, provinces),
        "available_genders": available_genders,
        "available_provinces": available_provinces,
        "records": [
            {"gender": str(r["gender"]), "province": str(r["province"]), "count": int(r["count"])}
            for r in matched
        ],
        "message": message,
    }
    return result


def _filter_line(result: Dict[str, object]) -> str:
    filters = result.get("filters") or {}
    gender = filters.get("gender") or "全部"
    province = filters.get("province") or "全部"
    return "性别=%s, 省份=%s" % (gender, province)


def _pct(part: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return "%.1f%%" % (100.0 * part / total)


def render_markdown(result: Dict[str, object]) -> str:
    """Render a query result as readable Markdown."""
    lines: List[str] = ["# 同名人数查询 (Same-Name Count)", ""]
    lines.append("- 姓名 Name: %s" % result["name"])
    lines.append("- 筛选 Filters: %s" % _filter_line(result))
    if not result.get("matched"):
        lines.append("- 结果 Result: 未找到匹配记录 (no match)")
        lines.append("")
        lines.append("> %s" % result.get("message", ""))
        return "\n".join(lines).rstrip() + "\n"
    total = int(result["total"])
    lines.append("- 同名人数 Total: %s" % f"{total:,}")
    by_gender = result.get("by_gender") or {}
    by_province = result.get("by_province") or {}
    lines.append("")
    lines.append("## 分维度统计 (Breakdown)")
    lines.append("")
    if by_gender:
        lines.append("### 按性别 By gender")
        for gender, count in by_gender.items():  # type: ignore[union-attr]
            lines.append("- %s: %s (%s)" % (gender, f"{count:,}", _pct(int(count), total)))
        lines.append("")
    if by_province:
        lines.append("### 按省份 By province")
        for province, count in by_province.items():  # type: ignore[union-attr]
            lines.append("- %s: %s (%s)" % (province, f"{count:,}", _pct(int(count), total)))
        lines.append("")
    lines.append("> 数据来源：内置示例数据集（demo data），仅供演示。")
    return "\n".join(lines).rstrip() + "\n"


def render_text(result: Dict[str, object]) -> str:
    """Render a query result as plain text."""
    lines: List[str] = ["同名人数查询 (Same-Name Count)", "=" * 30]
    lines.append("Name: %s | Filters: %s" % (result["name"], _filter_line(result)))
    if not result.get("matched"):
        lines.append("Result: no match")
        lines.append("Note: %s" % result.get("message", ""))
        return "\n".join(lines).rstrip() + "\n"
    total = int(result["total"])
    lines.append("Total: %s" % f"{total:,}")
    lines.append("")
    for gender, count in (result.get("by_gender") or {}).items():  # type: ignore[union-attr]
        lines.append("  By gender   %-4s %s" % (gender + ":", f"{count:,}"))
    for province, count in (result.get("by_province") or {}).items():  # type: ignore[union-attr]
        lines.append("  By province %-4s %s" % (province + ":", f"{count:,}"))
    lines.append("")
    lines.append("Source: built-in sample dataset (demo data)")
    return "\n".join(lines).rstrip() + "\n"


def render_json(result: Dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)


def render(result: Dict[str, object], fmt: str = "markdown") -> str:
    if fmt == "text":
        return render_text(result)
    if fmt == "json":
        return render_json(result)
    return render_markdown(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query same-name population counts from a built-in sample dataset.",
    )
    parser.add_argument("--name", default=None, help="name to look up (required unless --list-*), e.g. 张伟")
    parser.add_argument("--gender", default=None, help="filter by gender (男/女, or male/female)")
    parser.add_argument("--province", default=None, help="filter by province, e.g. 广东 or 广东省")
    parser.add_argument(
        "--format",
        choices=("markdown", "text", "json"),
        default="markdown",
        help="output format (default: markdown)",
    )
    parser.add_argument("--data", default=None, help="path to a custom dataset JSON")
    parser.add_argument("--output", default=None, help="write the result to a file instead of stdout")
    parser.add_argument("--list-provinces", action="store_true", help="list supported provinces and exit")
    parser.add_argument("--list-genders", action="store_true", help="list supported genders and exit")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = load_data(args.data)
    except (OSError, ValueError) as exc:
        print("error: cannot load dataset: %s" % exc, file=sys.stderr)
        return 2

    if args.list_genders:
        print(", ".join(str(g) for g in data["genders"]))
        return 0
    if args.list_provinces:
        print(", ".join(str(p) for p in data["provinces"]))
        return 0

    if not args.name or not str(args.name).strip():
        print("error: --name is required (unless using --list-provinces / --list-genders)", file=sys.stderr)
        return 2

    try:
        result = query(args.name, gender=args.gender, province=args.province, data=data)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    body = render(result, args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(body)
        print("Wrote result to %s" % args.output)
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())