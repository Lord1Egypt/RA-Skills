# curl 调用模板

> 用于快速 smoke test，不依赖 SDK。

## Moonshot / Kimi

```bash
curl https://api.moonshot.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -d '{
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

## 阿里云百炼

```bash
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

## SiliconFlow

```bash
curl https://api.siliconflow.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -d '{
    "model": "Pro/zai-org/GLM-4.7",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

## DeepSeek

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": false
  }'
```
