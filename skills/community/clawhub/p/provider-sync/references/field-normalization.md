# Field Normalization

本文件说明如何把上游模型列表规范化成 OpenClaw 可用的模型结构。只有在需要调整规范化策略、解释字段来源、或扩展模型能力映射时才读取。

## 目标结构

规范化后的模型通常包含：

- `id`
- `name`
- `api`
- `reasoning`
- `input`
- `cost`
- `contextWindow`
- `maxTokens`

## 基本映射原则

### id
优先从以下字段中选择：
- `id`
- `model`
- `name`

### name
优先从以下字段中选择：
- `name`
- `display_name`
- `title`
- 若都没有，则回退到 `id`

### reasoning
优先从以下字段判断：
- `reasoning`
- `supports_reasoning`
- `thinking`

未提供时默认 `false`。

### input
可能来自：
- `input`
- `modalities`
- `capabilities`

常见归一化：
- `vision` → `image`
- 其他值转成小写字符串
- 若没有可识别信息，默认 `['text']`

### contextWindow
可从以下字段取值：
- `contextWindow`
- `context_window`
- `context`
- `max_context_tokens`

取不到时使用默认值。

### maxTokens
可从以下字段取值：
- `maxTokens`
- `max_tokens`
- `max_output_tokens`
- `output_tokens`

取不到时使用默认值。

## 保留本地字段

如果启用 `--preserve-existing-model-fields`，优先保留本地同 id 模型上的这些字段：

- `name`
- `api`
- `reasoning`
- `input`
- `contextWindow`
- `maxTokens`
- `cost`

适用原因：
- 上游数据可能不完整
- 本地可能已经人工校准过能力参数
- 成本字段通常更适合本地维护

## 设计取舍

规范化的目标是“可用、稳定、可比较”，不是“完美还原上游全部语义”。

因此：
- 优先补齐 OpenClaw 必需字段
- 不追求一开始就支持所有供应商私有字段
- 对不稳定或临时字段保持保守，不要默认写入配置

## 规范化 profile

### auto
- 默认模式
- 按模型族系自动选择：
  - `gemini*` / 名称含 `gemini` → `gemini`
  - `gpt-*` / 名称含 `codex` → `gpt`
  - 其他 → `generic`
- 保持 provider-agnostic，不依赖某个部署环境里的 provider id 命名

### generic
- 保守模式
- 如果上游不给能力字段，通常回退到 `reasoning=false`、`input=['text']`

### gemini
- 适合 Gemini / gemini-compatible 上游
- 会对 `thinking` / `supportedGenerationMethods` / `vision` 等字段做更积极推断

### gpt
- 适合 GPT / Codex 系列
- 对已知模型 ID 使用固定能力模板，避免被 generic 口径冲回：
  - `gpt-5.4` / `gpt-5.4-mini` → `text,image` + `reasoning=true` + `400k` + `128k`
  - `gpt-5.2` / `gpt-5.2-codex` → `text,image` + `reasoning=true` + `400k` + `128k`
  - `gpt-5.3-codex` → `text` + `reasoning=true` + `400k` + `128k`
  - `gpt-5.1-codex-max` → `text` + `reasoning=true` + `400k` + `128k`
  - `gpt-5.1-codex-mini` → `text` + `reasoning=true` + `400k` + `32k`
- 对未显式收录但命中 `gpt-*` 的模型，会做温和推断：优先 `reasoning=true`，普通 GPT 默认 `text,image`，Codex 默认 `text`
