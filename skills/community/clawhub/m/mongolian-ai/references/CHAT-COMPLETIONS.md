# 对话补全

POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/chat/completions
Content-Type: application/json

messages 为 1–100 条消息，每条 role 为 system、user 或 assistant，content 必填且最多 4000 字符。可设置 system 消息要求只用中文、传统蒙古文或西里尔蒙古文回复；保留必要对话上下文。不要发送 from/to、model、temperature 或 max_tokens；模型参数由平台控制。

成功只提取 choices[0].message.content。不展示原始 JSON、内部系统消息或调试字段。
