#!/usr/bin/env python3
"""Prompt Harness -- 模板变量填充，生成 Subagent Prompt

通过模板 + 变量字典，动态生成 Subagent 的 Prompt。
支持嵌套变量、条件块、循环块。

用法:
  python prompt_harness.py --template references/tpl-outline.md \
      --var TOPIC="AI趋势" --var AUDIENCE="投资人" \
      --output runtime/prompt-step3.md

  python prompt_harness.py --template references/tpl-pageagent.md \
      --var PAGE_NUM=3 --var PLANNING=planning-3.json \
      --output runtime/prompt-pageagent-3.md
"""

import argparse
import re
import sys
from pathlib import Path


# -------------------------------------------------------------------
# 模板引擎
# -------------------------------------------------------------------
def render_template(template: str, variables: dict) -> str:
    """渲染模板，替换 {{VAR}} 和处理 {% if %} 块。"""

    # 处理条件块 {% if VAR %} ... {% endif %}
    def replace_conditional(match):
        var_name = match.group(1).strip()
        content = match.group(2)
        # 支持 {% if VAR %} 和 {% if not VAR %}
        negate = False
        if var_name.startswith("not "):
            negate = True
            var_name = var_name[4:].strip()

        value = variables.get(var_name)
        # 判断条件
        condition_met = bool(value) if not negate else not value
        return content if condition_met else ""

    # 递归处理嵌套条件块
    def handle_conditionals(text: str) -> str:
        pattern = re.compile(r'{%\s*if\s+([^%]+)%}(.*?){% endif %}', re.DOTALL)
        while pattern.search(text):
            text = pattern.sub(lambda m: replace_conditional(m), text)
        return text

    result = template

    # 处理条件块
    result = handle_conditionals(result)

    # 替换 {{VAR}} 变量
    def replace_var(match):
        var_name = match.group(1).strip()
        value = variables.get(var_name, "")
        if isinstance(value, (list, dict)):
            import json
            return json.dumps(value, ensure_ascii=False, indent=2)
        return str(value)

    result = re.sub(r'{{\s*([\w.]+)\s*}}', replace_var, result)

    # 清理未替换的变量
    result = re.sub(r'{{\s*[\w.]+\s*}}', '', result)

    # 清理空行
    result = re.sub(r'\n{3,}', '\n\n', result)

    return result.strip() + '\n'


def load_template(template_path: Path) -> str:
    """加载模板文件。"""
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def parse_var_string(var_str: str) -> tuple[str, str]:
    """解析 VAR=VALUE 格式。"""
    if '=' not in var_str:
        raise ValueError(f"Invalid variable format: {var_str}. Expected VAR=VALUE")
    key, value = var_str.split('=', 1)
    return key.strip(), value.strip()


# -------------------------------------------------------------------
# 主函数
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Prompt Harness -- Dynamic Prompt Generator")
    parser.add_argument("--template", "-t", type=Path, required=True,
                       help="Template file path")
    parser.add_argument("--var", "-v", action="append",
                       help="Variable in VAR=VALUE format (can be used multiple times)")
    parser.add_argument("--output", "-o", type=Path, required=True,
                       help="Output file path")
    parser.add_argument("--strict", action="store_true",
                       help="Fail if template file not found")

    args = parser.parse_args()

    try:
        template_content = load_template(args.template)
    except FileNotFoundError as e:
        if args.strict:
            raise
        print(f"WARNING: {e}", file=sys.stderr)
        sys.exit(1)

    # 解析变量
    variables = {}
    if args.var:
        for var_str in args.var:
            key, value = parse_var_string(var_str)
            variables[key] = value

    # 渲染
    result = render_template(template_content, variables)

    # 输出
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")

    print(f"Generated: {args.output} ({len(result)} chars)")
    if variables:
        print(f"Variables: {', '.join(variables.keys())}")


if __name__ == "__main__":
    main()
