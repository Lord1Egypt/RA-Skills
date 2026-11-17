# openai 模型适配器

<!--
MODEL-ADAPTER
id: openai
target: OpenAI GPT 系列(gpt-4o / o-series / gpt-5 系)
fingerprint_suffix: @model=openai
-->

> 唯一真相源:本文件定义 OpenAI GPT 系列目标模型的提示词结构改写规则。
> 正交性:适配器只改写**表达形态**,不改变 DEPTH 指纹的 9 位档位语义。

## 适用判定信号

- 用户显式指定 GPT / OpenAI / ChatGPT;
- 指纹后缀为 `@model=openai`;
- 需要 JSON 结构化输出或 function calling / tool use 场景。

## 结构偏好

用 Markdown 标题分层 + 输出契约区用 JSON Schema。GPT 系列对 `#` 层级与显式 JSON Schema 的遵循度最高。

| 通用段 | OpenAI 写法 |
|--------|------------|
| 角色 | `# Role` |
| 任务 | `# Task` |
| 上下文 | `# Context` |
| 示例 | `# Examples` |
| 输出格式 | `# Output Format` + JSON Schema 代码块 |
| 思考指令 | `# Reasoning Steps`(有序列表) |
| 约束 | `# Constraints`(正负面分列) |
| 自检 | `# Self-Check` |
| 迭代 | `# Iteration` |

## 必用写法

- 一级标题用 `#`,段落内用有序 / 无序列表分条目;
- 输出契约写成 JSON Schema(`{"type":"object","properties":{...},"required":[...]}`),并声明"仅输出符合该 Schema 的 JSON";
- 约束分两列:必须(MUST)与禁止(MUST NOT),逐条编号;
- o-series 推理模型:撤销"逐步思考"类指令,改为直接声明输出结构 —— 推理模型内部已链式思考,外部 CoT 指令会冗余甚至降质。

## 禁用写法

- 禁止用 XML 标签分段(GPT 系列对标签边界的遵循度低于 Markdown 层级);
- 禁止在需要 JSON 输出时同时给出"自由文本示例",会造成格式漂移;
- 禁止对 o-series 使用 `<thinking>` 类显式思考区(不被支持)。

## 注入模块

组装产出尾部追加:

```
## Output Contract
严格按以下 JSON Schema 输出,不要输出任何 Schema 之外的解释性文字:
```json
{ "type": "object", "required": ["<字段>"], "properties": { ... } }
```
```

## 与档位的交互

- D1/D2:Schema 可简化为字段清单列表;
- D3:Schema 必填 `required`,并给出错误码枚举;
- D4:追加对抗审查与复核节点字段,Schema 中显式声明 `assumptions` 数组。

## 质量检查清单

- [ ] 一级标题均为 Markdown `#` 形式
- [ ] 输出契约含完整 JSON Schema 且声明 required
- [ ] 约束分为 MUST / MUST NOT 两组
- [ ] o-series 场景未使用显式逐步思考指令
- [ ] DEPTH 头部指纹未被本适配器改写(仅尾部追加 Output Contract)
