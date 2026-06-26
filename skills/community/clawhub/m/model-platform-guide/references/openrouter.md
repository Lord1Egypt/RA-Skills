# OpenRouter API 参考摘要

> 精简版；以官方文档为准。
>
> 官方入口：
> - Docs: https://openrouter.ai/docs
> - API Keys: https://openrouter.ai/keys

## 速览

- 平台：OpenRouter
- 作用：统一接入多个模型供应商与模型路由
- 鉴权：Bearer Token
- OpenAI 兼容：通常是
- 常见 Base URL：`https://openrouter.ai/api/v1`
- 常见接口：`POST /chat/completions`

## 使用建议

OpenRouter 更像“聚合路由层”，回答时重点讲：

- 它不是单一模型供应商
- 模型名通常带供应商前缀/路由信息
- 适合做多模型统一接入和兜底

## 注意事项

- 文档页面结构可能变化，回答时优先引用 docs 首页
- 具体字段、模型与 header 以最新官方文档为准
