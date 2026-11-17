---
name: {{skill_name}}
description: "{{business_description}}。触发：{{trigger_phrase_1}} / {{trigger_phrase_2}} / {{trigger_phrase_3}} / {{trigger_phrase_4}} / {{trigger_phrase_5}}"
authored_by: linkfox-skill-creator
interview_record: references/interview-record.md
quality: {{quality_level}}
depends_on:
{{#each depends_on}}
  - {{this}}
{{/each}}
---

# {{skill_name}}

{{one_sentence_purpose_in_business_language}}

{{optional_second_paragraph_context}}

## 何时使用

{{#each typical_trigger_moments}}
- {{this}}
{{/each}}

## 何时不用

{{#each boundaries}}
- {{scenario}}
{{/each}}

{{#if has_depends_on}}
## 前置依赖

本能力需要以下现成小助手配合才能完整运行：

{{#each depends_on_with_names}}
- `{{slug}}` — {{business_name}}（{{purpose}}）
{{/each}}

首次使用前请确认这些小助手已安装。
{{/if}}

## 核心流程

{{#each process}}
### 步骤 {{step}}：{{name}}

{{#eq execution_type "script"}}
调用 `{{script}}`：

- **输入**：{{inputs_in_business_language}}
- **输出**：{{outputs_in_business_language}}
- **做什么**：{{one_line_business_description_of_script_purpose}}
{{/eq}}
{{#eq execution_type "delegate"}}
调用 `{{delegates_to}}` 这个 skill 完成。

- **入参**：
  {{#each delegate_inputs_mapping}}
  - {{@key}}：{{this_in_business_language}}
  {{/each}}
- **输出**：{{outputs_in_business_language}}
- **为什么用这个工具**：
  > {{delegate_expert_quote}}
{{/eq}}
{{#eq execution_type "llm"}}
{{judgmental_step_description_in_business_language}}

- **输入**：{{inputs_in_business_language}}
- **输出**：{{outputs_in_business_language}}
- **判断依据**：
  {{#each decisions}}
  - {{this}}
  {{/each}}
{{/eq}}

{{/each}}

## 关键规则

### 必须遵守
{{#each hard_rules}}
- {{text}}
{{/each}}

### 经验性（参考，非硬性）
{{#each soft_rules}}
- {{text}}
{{/each}}

## 典型踩坑

{{#each pitfalls}}
- **{{scenario}}** — {{why_wrong}}
{{/each}}

## 相关资料

- `references/workflow.md` — 流程细化与脚本调用
- `references/rules-and-boundaries.md` — 完整规则与边界
- `references/interview-record.md` — 原始访谈记录
{{#if has_scripts}}
- `scripts/` — 保证结果稳定的小程序
{{/if}}
