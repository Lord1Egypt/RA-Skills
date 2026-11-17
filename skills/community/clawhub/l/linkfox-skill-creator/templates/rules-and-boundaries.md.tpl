# 规则与边界

本文档整理了本 skill 涉及的所有规则（D4）和边界（D5）。规则决定"怎么做是对的"，边界决定"什么时候不该用这个能力"。

## 必须遵守的规则（硬规则）

{{#each hard_rules}}
### {{id}}：{{text}}

- **适用范围**：{{#each scope}}{{this}}{{#unless @last}}、{{/unless}}{{/each}}
{{#if counter_example}}
- **反例**：{{counter_example}}
{{else}}
- **反例**：无（硬规则，任何情况下都应遵守）
{{/if}}
- **专家原话**：
  > {{expert_verbatim}}

{{/each}}

## 经验性规则（软规则，可根据情况放宽）

{{#each soft_rules}}
### {{id}}：{{text}}

- **适用范围**：{{#each scope}}{{this}}{{#unless @last}}、{{/unless}}{{/each}}
- **反例**：{{counter_example}}
- **何时放宽**：{{when_to_relax}}
- **专家原话**：
  > {{expert_verbatim}}

{{/each}}

## 不适用场景（边界）

遇到以下情况，**应当放弃使用本 skill**，请用户自行处理或切换到其他能力：

{{#each boundaries}}
### {{id}}：{{scenario}}

- **为什么不适用**：{{why_not_applicable}}
- **该怎么办**：{{#if recommended_action}}{{recommended_action}}{{else}}明确告知用户本能力不覆盖此场景，不要硬撑强答{{/if}}
- **专家原话**：
  > {{expert_verbatim}}

{{/each}}

## 典型踩坑

以下是容易犯但不易察觉的错误，专家特别点名过：

{{#each pitfalls}}
### {{id}}：{{scenario}}

- **为什么是坑**：{{why_wrong}}
- **避免方法**：{{#if avoidance}}{{avoidance}}{{else}}每次执行到相关步骤时，多确认一次专家原话中的警示内容{{/if}}
- **专家原话**：
  > {{expert_verbatim}}

{{/each}}

## 规则优先级（冲突时如何取舍）

当两条规则冲突时，按以下优先级：

1. **安全性/合规性相关的硬规则** 最高优先
2. **业务效果相关的硬规则** 次之
3. **经验性（软）规则** 最低

边界规则是一票否决权：**任何一条边界触发都应立即停止本 skill 的执行**，无论其他规则怎么说。

## 与 interview-record 的对应关系

本文档的每一条规则 / 边界 / 踩坑都来自 `references/interview-record.md` 对应字段，保留了 `expert_verbatim` 作为原始依据。若后续评估报告指出"某条规则与专家原话不符"，以 interview-record.md 为准。
