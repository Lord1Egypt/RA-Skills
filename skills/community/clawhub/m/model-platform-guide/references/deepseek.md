# DeepSeek API 参考摘要

> 精简版；以官方文档为准。
>
> 官方入口：
> - https://api-docs.deepseek.com/
> - API Key: https://platform.deepseek.com/api_keys

## 速览

- 平台：DeepSeek
- 鉴权：`Authorization: Bearer $DEEPSEEK_API_KEY`
- OpenAI 兼容：是
- Base URL：`https://api.deepseek.com`
- OpenAI 兼容常见写法：`https://api.deepseek.com/v1`
- 典型接口：`POST /chat/completions`

## 最小 curl 示例

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "stream": false
  }'
```

## 常见模型

- `deepseek-chat`
- `deepseek-reasoner`

## 注意事项

- DeepSeek 文档明确说明接口格式兼容 OpenAI
- `v1` 只是兼容路径，不代表模型版本
- `deepseek-chat` 和 `deepseek-reasoner` 分别对应非思考/思考模式
