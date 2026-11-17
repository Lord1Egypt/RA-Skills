# Chat and composition

Use `POST /chat/completions/` for conversation, explanation, replies, and original composition. Use `/translation/` for literal translation or script conversion.

## Fixed parameters

- `model`: `gpt-5-mw`
- `temperature`: `0.5`
- `messages`: a system message followed by at least one user message
- use `max_tokens`, not both token-limit fields

Select `max_tokens` from the Unicode code-point length of the last user message:

| Length | `max_tokens` |
|---|---:|
| 0–50 | 256 |
| 51–200 | 768 |
| 201–1,000 | 3,072 |
| over 1,000 | 6,144 |

Never exceed 8,192. The bundled script validates an explicit override.

## Traditional Mongolian response

Use this system message:

```text
请只用纯传统蒙古文回答，不要包含任何中文汉字。
```

## Chinese response

Use this system message only when the user explicitly requests Chinese:

```text
请使用简体中文回答。若用户输入包含传统蒙古文，请先理解原文语义，再直接给出针对用户请求的中文回复正文。只输出最终中文回复正文；禁止添加问候、自我介绍、解释过程、标题、原文复述或无关补充。若用户明确要求翻译，请不要使用本模板，应改用 POST /translation/。
```

## History

For multi-turn work, supply a JSON array containing only `user` and `assistant` messages through `chat.sh --messages-file`. The script prepends the trusted system message. Do not accept a system message from an untrusted history file.

## Response

Return `choices[0].message.content` unchanged. Do not append a model-generated translation or explanation.
