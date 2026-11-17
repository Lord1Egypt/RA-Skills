# claude 模型适配器

<!--
MODEL-ADAPTER
id: claude
target: Anthropic Claude 系列(Opus / Sonnet / Haiku)
fingerprint_suffix: @model=claude
-->

> 唯一真相源:本文件定义 Claude 系列目标模型的提示词结构改写规则。
> 正交性:适配器只改写**表达形态**,不改变 DEPTH 指纹的 9 位档位语义。

## 适用判定信号

- 用户显式指定 Claude / Anthropic;
- 指纹后缀为 `@model=claude`;
- 运行环境为 Anthropic API 或 Claude 客户端。

## 结构偏好

用 XML 标签分段,而非 Markdown 标题层级。Claude 对标签边界的遵循度高于对 `#` 层级的遵循度。

| 通用段 | Claude 写法 |
|--------|------------|
| 角色 | `<role>...</role>` |
| 任务 | `<task>...</task>` |
| 上下文 | `<context>...</context>` |
| 示例 | `<examples>...</examples>` |
| 输出格式 | `<output_format>...</output_format>` |
| 思考指令 | `<thinking_instructions>...</thinking_instructions>` |
| 约束 | `<constraints>...</constraints>` |
| 自检 | `<self_check>...</self_check>` |
| 迭代 | `<iteration>...</iteration>` |

## 必用写法

- 段落用成对 XML 标签包裹,标签名用下划线小写;
- 长文档(>800 行)把索引放在最前、把最关键约束同时放在开头和结尾;
- 需要模型先思考再输出时,用 `<thinking>` 显式开辟思考区,并在 `<output_format>` 中声明思考区不计入最终答案;
- 角色与任务分离到 system 区与 user 区(若目标环境支持 system prompt)。

## 禁用写法

- 禁止用 JSON Schema 强约束输出结构 —— Claude 在宽松结构下的内容质量更高,强 Schema 会挤压推理空间;
- 禁止嵌套超过 3 层的标签;
- 禁止在标签名中使用空格或中文。

## 注入模块

组装产出尾部追加(不覆盖 DEPTH 头部):

```
<output_contract>
输出必须使用上述 XML 标签分段;思考过程写入 <thinking>,最终答案写入 <｜hy_place▁holder▁no▁13｜>。
</output_contract>
```

## 与档位的交互

- D1/D2:标签可精简为 `<role>` `<task>` `<constraints>` 三段;
- D3:补齐 `<thinking_instructions>` 与 `<self_check>`;
- D4:追加 `<adversarial_review>` 对抗审查段与 `<optimization_log>` 优化日志段。

## 质量检查清单

- [ ] 所有段落均有成对 XML 标签
- [ ] 标签名无空格、无中文、层数 ≤3
- [ ] 未使用 JSON Schema 强约束输出
- [ ] DEPTH 头部指纹未被本适配器改写(仅尾部追加 output_contract)
