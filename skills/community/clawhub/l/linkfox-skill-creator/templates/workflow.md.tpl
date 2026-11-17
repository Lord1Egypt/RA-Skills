# 工作流程

## 流程概览

```
{{input_representation}}
    ↓
{{#each process}}
步骤 {{step}}：{{name}}{{#eq execution_type "script"}}（脚本 {{script}}）{{/eq}}{{#eq execution_type "delegate"}}（委托 {{delegates_to}}）{{/eq}}{{#eq execution_type "llm"}}（经验判断）{{/eq}}
    ↓
{{/each}}
{{output_representation}}
```

{{#each process}}
## 步骤 {{step}}：{{name}}

- **类型**：{{#eq execution_type "script"}}固定规则（脚本执行）{{/eq}}{{#eq execution_type "delegate"}}委托现成能力（调用另一个 skill）{{/eq}}{{#eq execution_type "llm"}}经验判断（由 AI 理解上下文后处理）{{/eq}}
- **输入**：{{inputs_in_business_language}}
- **输出**：{{outputs_in_business_language}}

### 做什么

{{step_description_in_business_language}}

{{#eq execution_type "script"}}
### 脚本调用

执行 `{{script}}`：

**输入格式**（传入脚本）：
{{script_input_spec}}

**输出格式**（脚本返回）：
{{script_output_spec}}

**脚本的职责边界**（详见脚本开头的说明）：
{{script_scope_and_non_goals}}

{{/eq}}
{{#eq execution_type "delegate"}}
### 调用说明

{{#if delegates_to_is_tool_skill}}
`{{delegates_to}}` 是一个 **API 封装类工具 skill**，默认走 `api_call.py` 直接执行底层脚本并把 JSON 落盘，**不走 Skill 工具嵌套**（避免把大段数据灌进上下文）：

```bash
python scripts/api_call.py \
  ~/.claude/skills/{{delegates_to}}/scripts/{{tool_script_filename}} \
  ./data/step{{step}}_{{tool_short_tag}}.json \
  '{{params_json_string}}'
```

**入参来源**：
{{#each delegate_inputs_mapping}}
- `{{@key}}`：{{this_in_business_language}}
{{/each}}

**落盘文件**：`./data/step{{step}}_{{tool_short_tag}}.json`
**下游读取规则**：仅按需抽取子集字段（前 N 条 / 关键列），**不要**把整份 JSON 回注宿主上下文。

**stdout 摘要（宿主 LLM 只看这一行）示例**：
```json
{"status":"ok","output":".../data/step{{step}}_{{tool_short_tag}}.json","bytes":12345,"shape":{"type":"object","top_keys":["code","data","message"],"key_count":3}}
```

{{else}}
调用 `{{delegates_to}}` 这个 skill 完成本步（走 Skill 工具嵌套）。

**入参映射**：
{{#each delegate_inputs_mapping}}
- `{{@key}}`：{{this_in_business_language}}
{{/each}}

**输出**：{{outputs_in_business_language}}
{{/if}}

**专家为什么选这个工具**：

> {{delegate_expert_quote}}

**注意**：该子 skill 可能涉及账号或付费，首次使用前请确认权限与计费。

{{/eq}}
{{#eq execution_type "llm"}}
### 判断依据

{{#each decisions}}
- {{this}}
{{/each}}

### 经验参考

> {{expert_verbatim}}

{{/eq}}

### 决策点

{{#each decisions}}
- {{this}}
{{/each}}

{{#if assumed_fields_present}}
### 说明

以下部分是我根据上下文补齐，已经过专家确认：
{{#each assumed_fields}}
- {{this}}
{{/each}}
{{/if}}

{{/each}}

## 跨步骤的注意事项

- 若步骤 N 输出异常，步骤 N+1 应如何处理：**默认跳过并在最终报告中标记**
- 若整体失败：**保留已完成步骤的中间结果，便于后续排查**

## 外部依赖

{{#if has_external_dependencies}}
本流程涉及以下外部服务：

{{#each external_dependencies}}
- **{{service}}** — {{purpose}}（授权：{{auth_type}}，需要环境配置：{{env_vars}}）
{{/each}}

使用前请确认相关环境配置已就位。
{{else}}
本流程**不依赖**任何外部服务，纯本地推理和数据处理。
{{/if}}
