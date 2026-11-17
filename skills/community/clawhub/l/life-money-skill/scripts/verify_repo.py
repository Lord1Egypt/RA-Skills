#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Life Money Skill — 仓库自检（零依赖，可直接用于 CI）

三部分：
  1. 契约校验：examples/demo/*.json ↔ assets/schemas/*.schema.json
     支持 JSON Schema 子集：type / required / properties / items / enum / const /
     minimum / maximum / minItems / maxItems / minLength / maxLength
     —— 遇到白名单外的关键字直接报错（绝不静默放过，避免「假绿」）
  2. 渲染冒烟：调用 scripts/render_report.py 生成 report.html（输出到系统临时目录）
  3. 结构核对：报告关键组件计数与预期一致

用法：python scripts/verify_repo.py
退出码：0 = 通过；1 = 失败
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SUPPORTED_KEYWORDS = {
    "$schema", "$id", "title", "description", "type", "required", "properties",
    "items", "enum", "const", "minimum", "maximum", "minItems", "maxItems",
    "minLength", "maxLength", "additionalProperties", "format", "default",
}


def _is_type(data, name: str) -> bool:
    if name == "boolean":
        return isinstance(data, bool)
    if name == "integer":
        return isinstance(data, int) and not isinstance(data, bool)
    if name == "number":
        return isinstance(data, (int, float)) and not isinstance(data, bool)
    if name == "string":
        return isinstance(data, str)
    if name == "object":
        return isinstance(data, dict)
    if name == "array":
        return isinstance(data, list)
    if name == "null":
        return data is None
    return True


def _scan_keywords(schema, path: str, errs: list) -> None:
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k not in SUPPORTED_KEYWORDS:
                errs.append(f"校验器不支持关键字 `{k}`（位置 {path}）——请扩展校验器或改用完整 JSON Schema 校验")
            if k == "properties" and isinstance(v, dict):
                for pk, pv in v.items():
                    _scan_keywords(pv, f"{path}.properties.{pk}", errs)
            elif k == "items":
                _scan_keywords(v, f"{path}.items", errs)
    elif isinstance(schema, list):
        for i, s in enumerate(schema):
            _scan_keywords(s, f"{path}[{i}]", errs)


def validate_node(schema, data, path: str, errs: list) -> None:
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(data, x) for x in types):
            errs.append(f"{path}: 类型应为 {t}，实际 {type(data).__name__}")
            return
    if "const" in schema and data != schema["const"]:
        errs.append(f"{path}: 应为常量 {schema['const']!r}，实际 {data!r}")
    if "enum" in schema and data not in schema["enum"]:
        errs.append(f"{path}: 取值 {data!r} 不在枚举 {schema['enum']}")
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errs.append(f"{path}: {data} < minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errs.append(f"{path}: {data} > maximum {schema['maximum']}")
    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errs.append(f"{path}: 长度 {len(data)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errs.append(f"{path}: 长度 {len(data)} > maxLength {schema['maxLength']}")
    if isinstance(data, dict):
        for req in schema.get("required", []):
            if req not in data:
                errs.append(f"{path}: 缺少必填字段 `{req}`")
        for k, sub in (schema.get("properties") or {}).items():
            if k in data:
                validate_node(sub, data[k], f"{path}.{k}", errs)
    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errs.append(f"{path}: 元素数 {len(data)} < minItems {schema['minItems']}")
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errs.append(f"{path}: 元素数 {len(data)} > maxItems {schema['maxItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(data):
                validate_node(item_schema, item, f"{path}[{i}]", errs)


def check_contract(schema_path: Path, data_path: Path) -> list:
    """返回错误列表（空 = 通过）。"""
    errs: list = []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(data_path.read_text(encoding="utf-8"))
    _scan_keywords(schema, "$", errs)
    if errs:
        return errs
    validate_node(schema, data, "$", errs)
    return errs


CONTRACT_PAIRS = [
    ("assets/schemas/career_profile.schema.json", "examples/demo/profile.json"),
    ("assets/schemas/career_analysis.schema.json", "examples/demo/analysis.json"),
]

CHECKS = [
    ("隐藏技能卡片", 'class="skill__name"', 10),
    ("收入机会卡片", 'class="opp__title"', 10),
    ("变现路径项", 'class="path__name"', 5),
    ("高薪方向行", 'class="role__why"', 3),
    ("AI 副业卡片", 'class="svc__name"', 5),
    ("提示词卡", 'class="prompt__no"', 7),
    ("时间线节点", 'class="tl__name"', 3),
    ("内联 SVG", "<svg", 5),
    ("章节标题", "<h2>", 10),
]


def render_smoke():
    out = Path(tempfile.gettempdir()) / "life-money-smoke" / "report.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "render_report.py"),
            str(REPO / "examples" / "demo" / "analysis.json"),
            "--profile",
            str(REPO / "examples" / "demo" / "profile.json"),
            "--out",
            str(out),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    log = ((proc.stdout or "") + (proc.stderr or "")).strip().replace("\n", " | ")
    return proc.returncode == 0, log, out


def main() -> int:
    fails = []

    print("== 1. 契约校验 ==")
    for s_rel, d_rel in CONTRACT_PAIRS:
        errs = check_contract(REPO / s_rel, REPO / d_rel)
        if errs:
            fails.append(f"{d_rel} 违反 {s_rel}")
            for e in errs[:10]:
                print(f"   x {e}")
        else:
            print(f"   ok {d_rel} 符合 {s_rel}")

    print("== 2. 渲染冒烟 ==")
    ok, log, out = render_smoke()
    print(f"   {'ok' if ok else 'x '} {log}")
    if not ok:
        fails.append("渲染冒烟失败")

    print("== 3. 结构核对 ==")
    html = out.read_text(encoding="utf-8") if out.exists() else ""
    for name, pat, want in CHECKS:
        got = html.count(pat)
        good = got == want
        print(f"   {'ok' if good else 'x '} {name}：{got}（期望 {want}）")
        if not good:
            fails.append(f"{name} = {got}，期望 {want}")

    print()
    if fails:
        print("FAIL 校验未通过：")
        for f in fails:
            print("  -", f)
        return 1
    print("PASS 全部通过（契约 + 渲染 + 结构）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
