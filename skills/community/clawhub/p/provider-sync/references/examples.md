# Examples

本文件提供常见调用模板。只有在需要快速套用命令、演示 skill 用法、或补触发示例时才读取。

## 1. 同步某个 provider，先 dry-run

```bash
python3 scripts/provider_sync.py \
  --provider-id my-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --preserve-existing-model-fields \
  --dry-run
```

## 2. 探测兼容模式并给出推荐

```bash
python3 scripts/provider_sync.py \
  --provider-id my-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --probe-api-modes openai-responses,openai-completions \
  --dry-run
```

## 3. 用户确认后执行真实写入

```bash
python3 scripts/provider_sync.py \
  --provider-id my-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --preserve-existing-model-fields
```

## 4. 使用自定义 meta 接口

```bash
python3 scripts/provider_sync.py \
  --provider-id upstreamx \
  --endpoint https://api.example.com/provider/meta \
  --mapping-file references/mapping.example.json \
  --normalize-models \
  --dry-run
```

## 5. 只检查流程是否通，不写入

```bash
python3 scripts/provider_sync.py \
  --provider-id my-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --check-only
```

## 6. 只同步指定模型

```bash
python3 scripts/provider_sync.py \
  --provider-id my-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --include-model gpt-5 \
  --include-model gpt-5-mini \
  --dry-run
```

## 7. 输出 JSON 摘要

```bash
python3 scripts/provider_sync.py \
  --provider-id my-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --output json \
  --dry-run
```

## 8. Gemini 第三方代理 / 官方元数据接口

```bash
python3 scripts/provider_sync.py \
  --provider-id my-gemini \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --normalize-profile gemini \
  --preserve-existing-model-fields \
  --dry-run
```

> 如果上游主要是 Gemini 模型，即使不写 profile，`auto` 也会按模型族系自动走 `gemini`。

## 9. GPT / Codex provider（默认自动走 gpt）

```bash
python3 scripts/provider_sync.py \
  --provider-id my-gpt-provider \
  --endpoint https://api.example.com/v1/models \
  --mapping-file references/mapping.openai-models.json \
  --normalize-models \
  --preserve-existing-model-fields \
  --dry-run
```

如果上游主要是 GPT / Codex 模型，即使不写 profile，`auto` 也会按模型族系自动走 `gpt`；只有在想强制覆盖时，才需要显式带 `--normalize-profile gpt`。

## 10. 典型触发表达

以下说法都应该触发该 skill：

- “帮我把某个 provider 的模型从上游同步到 openclaw 配置里”
- “先 dry-run 看看这个 provider 会新增哪些模型”
- “拉一下上游模型列表，但保留我本地手工调过的能力字段”
- “帮我探测这个 provider 更适合 responses 还是 completions”
- “把 provider 配置同步流程整理成可复用的安全操作”
