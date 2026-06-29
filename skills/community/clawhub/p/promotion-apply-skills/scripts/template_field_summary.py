#!/usr/bin/env python3
"""
Summarize dynamic creative template fields from data-template-extract-private JSON.

Usage:
  mws link data-template-extract-private --env ${MWS_ENV} --params '{...}' --format json \
    | python3 template_field_summary.py
"""
import json
import sys


def load_json_from_stdin():
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("stdin is empty; pass template JSON")
    data = json.loads(raw)
    if isinstance(data, dict) and "data" in data:
        data = data["data"]
    if isinstance(data, list):
        if not data:
            raise SystemExit("template list is empty")
        return data[0]
    return data


def as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return bool(value)


def parse_condition_config(node):
    raw = node.get("conditionConfig") or "{}"
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw)
    except Exception:
        return {}


def summarize(template):
    print("模板：{} ({})".format(template.get("name", ""), template.get("id", "")))
    schema = template.get("schema") or {}
    if isinstance(schema, str):
        schema = json.loads(schema)
    for node in schema.get("children") or []:
        node_name = node.get("name") or node.get("code") or "默认节点"
        config = parse_condition_config(node)
        print("")
        print("节点：{}".format(node_name))
        for resource_type in node.get("resourceTypeCodes") or []:
            code = resource_type.get("code")
            print("资源类型：{}（{}）".format(resource_type.get("name", ""), code))
            for field in resource_type.get("resourceTypeFieldList") or []:
                field_name = field.get("fieldName")
                field_config = (config.get(code) or {}).get(field_name) or {}
                hidden = as_bool(field_config.get("hidden", False))
                selected = as_bool(field_config.get("select", False))
                required = as_bool(field_config.get("require", False))
                if hidden:
                    continue
                notes = []
                if selected:
                    notes.append("启用")
                if selected and required:
                    notes.append("必填")
                elif (not selected) and required:
                    notes.append("选填，模板未要求必填")
                elif not selected:
                    notes.append("选填，模板未要求")
                if field_config.get("width") and field_config.get("height"):
                    notes.append("尺寸 {}x{}".format(field_config["width"], field_config["height"]))
                if field_config.get("maxLength"):
                    notes.append("最多 {} 字".format(field_config["maxLength"]))
                if not notes:
                    notes.append("可选或模板预填")
                print(
                    "- {}：{}，{}，{}".format(
                        field.get("fieldChineseName") or field_name,
                        field_name,
                        field.get("uiType") or "",
                        "；".join(notes),
                    )
                )


def main():
    summarize(load_json_from_stdin())


if __name__ == "__main__":
    main()
