#!/usr/bin/env python3
"""
日志参数解析工具 v3

根据用户输入一段JSON和需要查找的参数，输出参数在JSON中的完整层级路径及枚举值，同时输出格式化后的JSON字符串。

特性：
- 多层嵌套JSON对象/数组递归搜索
- 自动解析JSON字符串字段（多层转义穿透）
- 外层JSON包含JSON字符串字段时的智能解析及修复
- 原始文本正则搜索（处理JSON解析失败场景）
- 参数名大小写/蛇形驼峰模糊匹配及自动重查
"""

import json
import re
import sys


def find_param_recursive(data, target, path="", depth=0, max_depth=20):
    """递归搜索参数在JSON中的位置"""
    results = []
    if depth > max_depth:
        return results

    if isinstance(data, dict):
        for key, val in data.items():
            cur = f"{path}.{key}" if path else key
            if key == target:
                results.append((cur, val))
            if isinstance(val, (dict, list)):
                results.extend(find_param_recursive(val, target, cur, depth + 1, max_depth))
            elif isinstance(val, str) and len(val) > 2:
                stripped = val.strip()
                if (stripped.startswith('{') and stripped.endswith('}')) or \
                   (stripped.startswith('[') and stripped.endswith(']')):
                    try:
                        parsed = json.loads(stripped)
                        if isinstance(parsed, (dict, list)):
                            results.extend(find_param_recursive(parsed, target, cur, depth + 1, max_depth))
                    except json.JSONDecodeError:
                        pass
    elif isinstance(data, list):
        for i, item in enumerate(data):
            cur = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                results.extend(find_param_recursive(item, target, cur, depth + 1, max_depth))
            elif isinstance(item, str) and len(item) > 2:
                stripped = item.strip()
                if (stripped.startswith('{') and stripped.endswith('}')) or \
                   (stripped.startswith('[') and stripped.endswith(']')):
                    try:
                        parsed = json.loads(stripped)
                        if isinstance(parsed, (dict, list)):
                            results.extend(find_param_recursive(parsed, target, cur, depth + 1, max_depth))
                    except json.JSONDecodeError:
                        pass
    return results


def repair_json_string(s):
    """尝试修复常见的JSON字符串问题"""
    if not isinstance(s, str):
        return None, False
    stripped = s.strip()
    try:
        return json.loads(stripped), True
    except json.JSONDecodeError:
        pass

    if stripped.startswith('{') or stripped.startswith('['):
        for i in range(5):
            fixed = stripped + '}' * (i + 1)
            try:
                return json.loads(fixed), True
            except json.JSONDecodeError:
                pass
            if stripped.startswith('['):
                fixed = stripped + ']' * (i + 1)
                try:
                    return json.loads(fixed), True
                except json.JSONDecodeError:
                    pass

    if '\\"' in stripped:
        fixed = stripped.replace('\\"', '\\\\"')
        try:
            return json.loads(fixed), True
        except json.JSONDecodeError:
            pass
        for i in range(3):
            try:
                return json.loads(fixed + '}' * (i + 1)), True
            except json.JSONDecodeError:
                pass

    return None, False


def load_json_input(input_str):
    """尝试多种方式加载JSON输入，返回 (parsed_object, has_inner_parse)"""
    parsed = None
    try:
        parsed = json.loads(input_str)
    except json.JSONDecodeError:
        pass

    if parsed is None:
        parsed, ok = repair_json_string(input_str)
        if not ok:
            parsed = None

    has_inner = False
    if isinstance(parsed, dict):
        for key in list(parsed.keys()):
            val = parsed[key]
            if isinstance(val, str) and len(val) > 10:
                if val.strip().startswith('{') or val.strip().startswith('['):
                    inner, ok = repair_json_string(val)
                    if ok and isinstance(inner, (dict, list)):
                        parsed = dict(parsed)
                        parsed[key] = inner
                        has_inner = True
        return parsed, has_inner

    if parsed is not None:
        return parsed, True
    return input_str, False


def find_parent_path(text, pos):
    """在JSON字符串中，从给定位置向前遍历，找出父级key的层级路径"""
    before = text[:pos]
    depth = 0
    i = 0
    last_key = None
    stack = []
    while i < len(before):
        c = before[i]
        if c == '\\':
            i += 2
            continue
        if c == '"':
            j = i + 1
            while j < len(before):
                if before[j] == '\\':
                    j += 2
                    continue
                if before[j] == '"':
                    break
                j += 1
            key_candidate = before[i+1:j]
            k = j + 1
            while k < len(before) and before[k] in ' \t\n\r':
                k += 1
            if k < len(before) and before[k] == ':':
                last_key = key_candidate
            i = j + 1
            continue
        if c == '{':
            depth += 1
            if last_key:
                stack.append((depth, last_key))
        elif c == '}':
            if depth > 0:
                depth -= 1
        i += 1
    path_parts = []
    for d, k in stack:
        if k:
            path_parts.append(k)
    return '.'.join(path_parts)


def find_param_in_raw_json(text, target):
    """在原始JSON字符串中查找参数（支持转义引号内的key）"""
    results = []
    pattern1 = rf'"{re.escape(target)}"\s*:\s*("[^"]*"|\d+(?:\.\d+)?|true|false|null)'
    pattern2 = rf'\\"{re.escape(target)}\\"' + r'\s*:\s*([^,}\]]+|"[^"]*"|\d+)'
    for pattern in (pattern1, pattern2):
        for match in re.finditer(pattern, text):
            path = find_parent_path(text, match.start())
            val = match.group().split('":', 1)[1].strip().strip('"')
            if not path and '\\"' in match.group():
                raw_before = text[:match.start()]
                path = find_parent_path(raw_before.replace('\\"', '"'), match.start())
            if path:
                results.append((f"{path}.{target}", val))
            else:
                results.append((f"{target}", val))
    return results


def find_similar_keys(raw_text, target, json_obj=None):
    """模糊匹配类似key名"""
    all_keys = set()
    for m in re.finditer(r'"([a-zA-Z_][a-zA-Z0-9_]*)"\s*:', raw_text):
        all_keys.add(m.group(1))
    for m in re.finditer(r'\\"([a-zA-Z_][a-zA-Z0-9_]*)\\"' + r'\s*:', raw_text):
        all_keys.add(m.group(1))
    if json_obj and isinstance(json_obj, (dict, list)):
        def collect_keys(obj):
            keys = set()
            if isinstance(obj, dict):
                for k, v in obj.items():
                    keys.add(k)
                    if isinstance(v, (dict, list)):
                        keys.update(collect_keys(v))
            elif isinstance(obj, list):
                for item in obj:
                    keys.update(collect_keys(item))
            return keys
        all_keys.update(collect_keys(json_obj))

    if not all_keys:
        return []

    suggestions = []
    candidates = {target}
    snake1 = re.sub(r'([A-Z])([A-Z])', r'\1_\2', target)
    snake2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', snake1)
    candidates.add(snake2.lower())
    camel = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), target)
    candidates.add(camel)
    candidates.add(camel[0].upper() + camel[1:] if camel else camel)

    target_lower = target.lower()
    for key in all_keys:
        if key == target:
            suggestions.append((key, 'exact'))
        elif key in candidates:
            suggestions.append((key, 'snake_camel'))
        elif key.lower() == target_lower:
            suggestions.append((key, 'case'))
        # 去下划线后匹配: reply_id ↔ replyid
        elif key.replace('_', '').lower() == target_lower:
            suggestions.append((key, 'snake_camel'))
        # 去连字符后匹配
        elif key.replace('-', '').lower() == target_lower:
            suggestions.append((key, 'snake_camel'))
        elif target_lower in key.lower() or key.lower() in target_lower:
            suggestions.append((key, 'partial'))
    return suggestions


def format_value(val):
    if isinstance(val, str):
        return val
    elif isinstance(val, (int, float, bool)):
        return str(val)
    elif val is None:
        return "null"
    else:
        return json.dumps(val, ensure_ascii=False)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("用法:")
        print("  python3 json_param_parser.py '<json_string>' <param_name>")
        print("  python3 json_param_parser.py -f <json_file> <param_name>")
        print("  echo '<json>' | python3 json_param_parser.py - <param_name>")
        sys.exit(1)

    json_data = None
    param_name = None
    raw_input = None

    if sys.argv[1] == '-f' and len(sys.argv) >= 4:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            raw_input = f.read()
        param_name = sys.argv[3]
    elif sys.argv[1] == '-' and len(sys.argv) >= 3:
        raw_input = sys.stdin.read()
        param_name = sys.argv[2]
    elif len(sys.argv) >= 3:
        raw_input = sys.argv[1]
        param_name = sys.argv[2]

    if not raw_input or not param_name:
        print("错误：参数不足", file=sys.stderr)
        sys.exit(1)

    json_data, has_inner_parse = load_json_input(raw_input)

    results = []
    if isinstance(json_data, dict) and has_inner_parse:
        for key, val in json_data.items():
            if isinstance(val, (dict, list)):
                inner_results = find_param_recursive(val, param_name, key)
                results.extend(inner_results)
            elif key == param_name:
                results.append((key, val))
        results.extend(find_param_recursive(json_data, param_name))
    elif isinstance(json_data, str):
        results = find_param_in_raw_json(json_data, param_name)
    else:
        results = find_param_recursive(json_data, param_name)
        raw_results = find_param_in_raw_json(raw_input, param_name)
        results.extend(raw_results)

    if results:
        seen = set()
        unique_results = []
        for path, value in results:
            k = (path, str(value))
            if k not in seen:
                seen.add(k)
                unique_results.append((path, value))
        results = unique_results

        print(">>> 参数查询结果：")
        print(f"查询参数: {param_name}")
        print(f"匹配数: {len(results)}")
        print()
        for path, value in results:
            print(f"  {path}  =  {format_value(value)}")
        return

    # 兜底: 原始文本搜索
    results = find_param_in_raw_json(raw_input, param_name)
    if results:
        print(">>> 参数查询结果：")
        print(f"查询参数: {param_name}")
        print(f"匹配数: {len(results)}")
        print()
        for path, value in results:
            print(f"  {path}  =  {value}")
        return

    # 模糊匹配
    suggestions = find_similar_keys(raw_input, param_name, json_data)
    priority = {'exact': 0, 'snake_camel': 1, 'case': 2, 'partial': 3}
    suggestions.sort(key=lambda x: (priority.get(x[1], 99), x[0]))

    if suggestions:
        for key, match_type in suggestions:
            if match_type in ('snake_camel', 'case', 'exact'):
                if isinstance(json_data, dict) and not isinstance(json_data, str):
                    results = find_param_recursive(json_data, key)
                if results:
                    print(f">>> 参数查询结果（'{param_name}'未找到，自动匹配相似参数'{key}'）：")
                    print(f"查询参数: {param_name} → 实际字段: {key}")
                    print(f"匹配数: {len(results)}")
                    print()
                    for path, value in results:
                        print(f"  {path}  =  {format_value(value)}")
                    return

        if not results:
            for key, match_type in suggestions:
                if match_type in ('snake_camel', 'case', 'exact'):
                    results = find_param_in_raw_json(raw_input, key)
                    if results:
                        print(f">>> 参数查询结果（'{param_name}'未找到，自动匹配相似参数'{key}'）：")
                        print(f"查询参数: {param_name} → 实际字段: {key}")
                        print(f"匹配数: {len(results)}")
                        print()
                        for path, value in results:
                            print(f"  {path}  =  {value}")
                        return

        print(f"未找到参数 '{param_name}'")
        print("以下为相似参数名，请检查：", file=sys.stderr)
        shown = set()
        for key, match_type in suggestions:
            if key not in shown:
                shown.add(key)
                label = {'snake_camel': '蛇形/驼峰', 'case': '大小写', 'partial': '部分匹配'}.get(match_type, match_type)
                print(f"  - {key} ({label})", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"未找到参数 '{param_name}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
