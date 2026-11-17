# -*- coding: utf-8 -*-
"""结构化输出校验：读 schema(JSON) + 待校验文本/文件，逐维 pass/fail + 修复提示。零依赖。"""
import argparse, json, pathlib, re

def load_json_text(s):
    s = s.strip()
    # 容忍 ```json 代码块包裹
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", s)
    if m:
        s = m.group(1)
    try:
        return json.loads(s), None
    except Exception as e:
        return None, f"JSON 解析失败: {e}"

def check_type(val, t):
    if t == "str":
        return isinstance(val, str)
    if t == "int":
        return isinstance(val, int) and not isinstance(val, bool)
    if t == "float":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if t == "bool":
        return isinstance(val, bool)
    if t == "list":
        return isinstance(val, list)
    if t == "dict":
        return isinstance(val, dict)
    return True

def validate(obj, schema):
    issues = []
    required = schema.get("required", [])
    fields = schema.get("fields", {})
    for f in required:
        if f not in fields:
            fields[f] = {"required": True}
    for name, spec in fields.items():
        must = spec.get("required", name in required)
        present = obj is not None and name in obj and obj[name] is not None
        if must and not present:
            issues.append({"field": name, "expected": "存在(必填)", "got": "缺失", "hint": f"补充必填字段 {name}"})
            continue
        if not present:
            continue
        val = obj[name]
        t = spec.get("type")
        if t and not check_type(val, t):
            issues.append({"field": name, "expected": t, "got": type(val).__name__, "hint": f"{name} 应为 {t}"})
        enum = spec.get("enum")
        if enum and val not in enum:
            issues.append({"field": name, "expected": "∈ " + str(enum), "got": val, "hint": f"{name} 取值需在枚举内"})
    return issues

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    schema = json.loads(pathlib.Path(a.schema).read_text(encoding="utf-8-sig"))
    if a.text:
        src = a.text
    else:
        src = pathlib.Path(a.file).read_text(encoding="utf-8-sig")

    obj, err = load_json_text(src)
    if err:
        issues = [{"field": "(root)", "expected": "合法 JSON", "got": "解析失败", "hint": err}]
        print(json.dumps({"pass": False, "issues": issues}, ensure_ascii=False, indent=2) if a.json else f"❌ {err}")
        return

    issues = validate(obj, schema)
    if a.json:
        print(json.dumps({"pass": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        print(f"校验：{'✅ 通过' if not issues else '🔒 拦截'}  问题：{len(issues)}")
        for i in issues:
            print(f"  [{i['field']}] 期望 {i['expected']} | 实际 {i['got']} | 修复：{i['hint']}")

if __name__ == "__main__":
    main()
