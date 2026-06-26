# Provider Patterns

本文件说明常见上游 provider 接入模式。只有在需要新增接入方式、修改探测逻辑、或理解某类 provider 返回结构时才读取。

## 目录

1. OpenAI-compatible `/models`
2. Provider meta endpoint
3. Custom nested payload
4. API mode probing

## 1. OpenAI-compatible `/models`

适用场景：
- 上游暴露 `/v1/models` 或兼容接口
- 响应主体通常包含 `data: []`
- 每个模型至少有 `id`

常见特点：
- 可直接把 `data` 映射到 `.models`
- 往往需要再做规范化，补齐 `input` / `reasoning` / `contextWindow` / `maxTokens`
- 同一 provider 可能同时兼容 `openai-responses` 和 `openai-completions`

推荐：
- 如果使用默认 `references/mapping.openai-models.json`，不要再额外设 `response-root=data`（该 mapping 本身已经从 `data` 取模型列表）
- 同时启用 `--normalize-models`
- 默认让脚本按模型族系自动选 profile：`gemini* -> gemini`，`gpt-* / *codex* -> gpt`，其他回退 `generic`
- 只有在需要覆盖默认行为时，再显式传 `--normalize-profile gemini|gpt|generic`
- 如不确定兼容模式，启用 `--probe-api-modes`

## 2. Provider meta endpoint

适用场景：
- 上游不是标准 `/models`
- 返回 provider 级元数据，如 `baseUrl`、`supportedApis`、`models`、`limits`

常见特点：
- 一个响应里同时包含 provider 字段和模型字段
- 更适合通过 mapping file 分开写入不同路径

推荐：
- 把 provider 级字段与模型列表字段分开映射
- 尽量只同步稳定字段，不要把临时状态字段写入本地配置

## 3. Custom nested payload

适用场景：
- 响应结构很深，例如 `payload.models.items`
- 不同字段命名差异较大

常见做法：
- 使用 `response-root` 先切到某个子树
- 再通过 mapping file 的 `from` 路径取值

建议：
- mapping 保持简短明确
- 如果映射规则开始变得复杂，优先把复杂逻辑加到脚本里，不要在 skill 里堆说明

## 4. API mode probing

目的：
- 判断一个 provider 更适合配置为哪种 `provider.api`

当前可探测模式示例：
- `openai-responses`
- `openai-completions`

解释原则：
- `404/405`：通常表示该模式不支持
- 其他 HTTP 错误：通常表示接口存在，但请求参数、权限或模型不匹配
- 第一个被判定为 supported 的模式可作为推荐值，但不是绝对真理

注意：
- 探测结果用于“推荐”，不要把它表述成完全确定的事实
- 如果 provider 文档与探测结果冲突，以用户明确要求或官方文档为准
