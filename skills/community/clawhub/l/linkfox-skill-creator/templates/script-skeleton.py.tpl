#!/usr/bin/env python3
"""
{{step_name_in_business_language}}

做什么：
  {{one_or_two_sentence_description}}

输入（stdin JSON）：
  {
    {{#each inputs}}
    "{{name}}": "{{type}}"{{#unless @last}},{{/unless}}  # {{note}}
    {{/each}}
  }

输出（stdout JSON）：
  {
    {{#each outputs}}
    "{{name}}": "{{type}}"{{#unless @last}},{{/unless}}  # {{note}}
    {{/each}}
  }

不做：
{{#each non_goals}}
  - {{this}}
{{/each}}

来源：
  本脚本对应 {{skill_name}} 的步骤 {{step_number}}「{{step_name}}」。
  专家原话见 references/interview-record.md 的 process[{{step_index}}].expert_verbatim。
"""

import json
import sys


def {{function_name}}(
    {{#each inputs}}
    {{name}}: {{python_type}}{{#unless @last}},{{/unless}}
    {{/each}}
) -> dict:
    """核心判定逻辑。"""
    {{#if has_extractable_logic}}
    # 专家明确表达过的规则——直接实现
    {{#each expert_rules}}
    {{rule_as_python_condition}}
    {{/each}}
    {{else}}
    # TODO: 专家描述中未提供可形式化的判断逻辑
    #   建议与专家对齐后补全，或改为 deterministic=false 交回 LLM 处理
    raise NotImplementedError("逻辑待专家补充")
    {{/if}}


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"输入不是合法 JSON: {e}"}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(2)

    try:
        result = {{function_name}}(
            {{#each inputs}}
            data.get("{{name}}", {{default_value}}){{#unless @last}},{{/unless}}
            {{/each}}
        )
    except NotImplementedError as e:
        print(json.dumps({"error": str(e), "status": "todo"}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(json.dumps({"error": f"执行失败: {e}"}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(1)

    json.dump(result, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
