#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_schema.py — 输出契约最小验证器（v7.7.0 新增；零依赖）

验证引擎输出是否符合 schemas/*.schema.json 契约。支持子集：
type / required / properties / items / enum / minimum / maximum / additionalProperties=false。
不追求完整 JSON Schema 实现——只承诺契约文件用到的子集；超出子集的键会被
--selfcheck 报 unsupported 并 FAIL（契约文件不能悄悄用到未实现的关键字）。

用法:
  python3 scripts/pp_schema.py --selfcheck          # 用真引擎输出自证四契约
  python3 scripts/pp_schema.py validate <schema> <json文件>
  python3 scripts/pp.py schema --selfcheck          # 同 selfcheck
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMAS = HERE.parent / "schemas"

_SUPPORTED = {"type", "required", "properties", "items", "enum",
              "minimum", "maximum", "additionalProperties", "$schema", "$id",
              "title", "description", "$ref"}


class SchemaError(Exception):
    pass


def _type_ok(value, t):
    if isinstance(t, list):
        return any(_type_ok(value, x) for x in t)
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    raise SchemaError(f"unsupported type keyword: {t}")


def validate(obj, schema, path="$"):
    """验证 obj 符合 schema（支持的子集），违规抛 SchemaError（信息带路径）。"""
    unknown = set(schema) - _SUPPORTED
    if unknown:
        raise SchemaError(f"{path}: schema 用了未实现的关键字 {sorted(unknown)}"
                          "（契约子集外——要么实现它，要么改契约）")
    if "enum" in schema and obj not in schema["enum"]:
        raise SchemaError(f"{path}: {obj!r} 不在枚举 {schema['enum']}")
    if "minimum" in schema and isinstance(obj, (int, float)) and obj < schema["minimum"]:
        raise SchemaError(f"{path}: {obj} < minimum {schema['minimum']}")
    if "maximum" in schema and isinstance(obj, (int, float)) and obj > schema["maximum"]:
        raise SchemaError(f"{path}: {obj} > maximum {schema['maximum']}")
    t = schema.get("type")
    if t is not None and not _type_ok(obj, t):
        raise SchemaError(f"{path}: 类型不符（期望 {t}，实得 {type(obj).__name__}）")
    if isinstance(obj, dict):
        for req in schema.get("required", []):
            if req not in obj:
                raise SchemaError(f"{path}: 缺必填键 {req}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(obj) - set(props)
            if extra:
                raise SchemaError(f"{path}: 多出未声明键 {sorted(extra)}")
        for k, sub in props.items():
            if k in obj:
                validate(obj[k], sub, f"{path}.{k}")
    if isinstance(obj, list) and "items" in schema:
        for i, item in enumerate(obj):
            validate(item, schema["items"], f"{path}[{i}]")


def _real_outputs():
    """真引擎样本（进程内同源）。"""
    sys.path.insert(0, str(HERE))
    import pp_api
    text = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
            "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
            "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
            "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
            "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")
    return {
        "detect": pp_api.detect_text(text),
        "fix_suggest": pp_api.fix_suggest(text),
        "workflow": pp_api.workflow(text),
        "term_report": pp_api.term_report(text),
    }


def selfcheck():
    """真引擎输出逐一过契约——契约与实现漂移当场暴露。"""
    outs = _real_outputs()
    failed = []
    for name in ("detect", "fix_suggest", "workflow", "term_report"):
        schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
        try:
            validate(outs[name], schema)
            print(f"[PASS] {name} 输出符合契约 {name}.schema.json")
        except SchemaError as e:
            print(f"[FAIL] {name}: {e}")
            failed.append(name)
    if failed:
        print(f"自证 FAIL：{failed}（契约与实现漂移——修实现或修契约，二选一并声明）",
              file=sys.stderr)
        return 1
    print("输出契约自证 PASS（4/4）")
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--selfcheck":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
        return selfcheck()
    if args[0] == "validate" and len(args) >= 3:
        schema = json.loads(Path(args[1]).read_text(encoding="utf-8"))
        obj = json.loads(Path(args[2]).read_text(encoding="utf-8"))
        try:
            validate(obj, schema)
            print("PASS")
            return 0
        except SchemaError as e:
            print(f"FAIL: {e}", file=sys.stderr)
            return 1
    print("用法见 --help", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
