#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _get(d: Dict[str, Any], path: List[str], default: Any = None) -> Any:
    cur: Any = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def build_natural_language(resp: Dict[str, Any]) -> str:
    """
    将评估接口返回（aortic_surgery 等）组装为自然语言。
    关注点：
    - final_result（satisfied + reason）
    - conditions[*].evidence（以及可选 source / reasoning / description）
    """
    if not resp.get("success"):
        err = resp.get("error") or _get(resp, ["result", "error"]) or "接口返回 success=false"
        return f"评估失败：{err}"

    result = resp.get("result") or {}
    criteria_name = result.get("criteria_name") or result.get("disease_type") or "评估项目"

    final_satisfied = _get(result, ["final_result", "satisfied"], None)
    final_reason = _get(result, ["final_result", "reason"], "") or ""

    if final_satisfied is True:
        conclusion = f"结论：符合{criteria_name}理赔条件。"
    elif final_satisfied is False:
        conclusion = f"结论：不符合{criteria_name}理赔条件。"
    else:
        conclusion = f"结论：{criteria_name}评估结果未知。"

    if final_reason.strip():
        conclusion += f"原因：{final_reason.strip()}。"

    conditions = result.get("conditions") or []
    evidences: List[str] = []
    for idx, c in enumerate(conditions, start=1):
        if not isinstance(c, dict):
            continue
        satisfied = c.get("satisfied")
        evidence = (c.get("evidence") or "").strip()
        source = (c.get("source") or "").strip()
        description = (c.get("description") or "").strip()

        prefix = f"{idx})"
        status = "满足" if satisfied is True else ("不满足" if satisfied is False else "未知")

        parts: List[str] = []
        if description:
            parts.append(description)
        if evidence:
            parts.append(f"证据：{evidence}")
        if source:
            parts.append(f"来源：{source}")

        if parts:
            evidences.append(f"{prefix}{status}，" + "；".join(parts))
        else:
            evidences.append(f"{prefix}{status}")

    if evidences:
        return conclusion + "\n依据：\n" + "\n".join(evidences)
    return conclusion


def main() -> int:
    parser = argparse.ArgumentParser(description="Format assessment response to natural language.")
    parser.add_argument("--input", required=True, help="Path to assessment response JSON.")
    parser.add_argument("--output", default="", help="Optional output text file path.")
    args = parser.parse_args()

    in_path = Path(args.input)
    resp = json.loads(in_path.read_text(encoding="utf-8"))
    text = build_natural_language(resp)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

