# MiniMax API 参考摘要

> 精简版；以官方文档为准。
>
> 官方入口：
> - 文档首页：https://platform.minimaxi.com/docs
> - 文本生成接口：https://platform.minimaxi.com/docs/api-reference/text-post
> - 索引：https://platform.minimaxi.com/docs/llms.txt

## 速览

- 平台：MiniMax
- Base URL：`https://api.minimaxi.com`
- 典型接口：`POST /v1/text/chatcompletion_v2`
- 鉴权：Bearer Token

## 文档中可见的关键信息

- 当前文档页显示的接口为：`/v1/text/chatcompletion_v2`
- 示例模型名：`MiniMax-M2.7`
- 支持流式输出
- 支持图文输入
- 响应中可见 `reasoning_tokens`

## 使用建议

回答 MiniMax 时，优先给：

1. 官方文档入口
2. Base URL
3. 典型 endpoint
4. 最小请求示例

## 注意事项

- MiniMax 的接口路径和 OpenAI 标准路径不同，不能想当然套 `/chat/completions`
- 模型名也和其他平台差异较大
