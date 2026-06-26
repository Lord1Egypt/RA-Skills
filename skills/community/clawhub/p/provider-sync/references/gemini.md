# Gemini Notes

本文件说明 provider-sync 在 Gemini 场景下的使用边界与推荐方式。只有在接入 Google 官方 Gemini 或 Gemini 第三方代理时才读取。

## 推荐分两类看

### 1. OpenAI-compatible Gemini
如果上游虽然是 Gemini，但暴露的是 OpenAI-compatible 接口，例如：
- `/v1/models`
- 返回 `data: [...]`

这种是 provider-sync 最容易处理的 Gemini 场景。

推荐：
- 使用 `references/mapping.openai-models.json`
- 启用 `--normalize-models`
- 如模型字段较少，启用 `--normalize-profile gemini`
- 如接口本身兼容 OpenAI，再考虑 `--probe-api-modes`

## 2. Google 官方或自定义 Gemini 元数据接口
如果上游不是 OpenAI-compatible，而是原生 Gemini 风格或自定义 JSON：
- 先用 `response-root` + `mapping-file` 把模型列表映射出来
- 再用 `--normalize-models --normalize-profile gemini` 做能力字段补齐

## Gemini profile 会做什么

`--normalize-profile gemini` 目前是轻量适配，不会替代 mapping，也不会假装知道所有 Gemini 私有语义。

当前行为：
- 优先识别 `inputTokenLimit` / `outputTokenLimit`
- 识别 `supportedGenerationMethods`
- 对 `gemini-*` 模型在缺少模态信息时保守推断为 `text,image`
- 对名称或 id 中包含 `thinking` / `reasoning` 的模型推断 reasoning=true

## 不要过度承诺

Gemini profile 的目标是“更可用”，不是“100% 还原官方能力矩阵”。

因此：
- 优先补齐 OpenClaw 需要的关键字段
- 不自动推断过多私有能力
- 如果官方文档与推断冲突，以显式文档或用户指定值为准

## 建议

- 对 Gemini 官方原生接口，不要默认把 OpenAI probe 结果当成真实结论
- 如果接口根本不是 OpenAI-compatible，可以跳过 `--probe-api-modes`
- 如果你已经手工校准过模型能力字段，优先加 `--preserve-existing-model-fields`
