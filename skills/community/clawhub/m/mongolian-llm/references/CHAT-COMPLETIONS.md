# `POST /chat/completions/`

路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

互译一律 **`POST /translation/`**，禁止本接口代译（契约/计费不同）。蒙语对话、说明、从零写蒙文等。

## `max_tokens`

最后一条 `role: user` 的 `content` 数 **Unicode 码点** `L`（勿用 JS `string.length` 当码点）。

| **`L`** | **`max_tokens`** |
|--------|------------------|
| ≤ 50 | **256** |
| 51～200 | **768**（或 **512** 控成本） |
| 201～1000 | **3072**（或 **4096**） |
| > 1000 | **8192**（可先 **6144**） |

封顶 **8192**；`max_completion_tokens` 与 `max_tokens` 二选一。

## 固定参数

| 参数 | 值 |
|------|-----|
| `model` | **`gpt-5-mw`** |
| `temperature` | **`0.5`** |
| `messages` | 须含 `user`；`system` 见下 |

## 模板

**传统蒙古文**

```json
{
  "model": "gpt-5-mw",
  "messages": [
    {"role": "system", "content": "请只用纯传统蒙古文回答，不要包含任何中文汉字。"},
    {"role": "user", "content": "<用户问题>"}
  ],
  "temperature": 0.5,
  "max_tokens": 768
}
```

**中文回复**（用户明确要求中文输出时）

```json
{
  "model": "gpt-5-mw",
  "messages": [
    {"role": "system", "content": "请使用简体中文回答。若用户输入包含传统蒙古文，请先理解原文语义，再直接给出针对用户请求的中文回复正文。只输出最终中文回复正文；禁止添加问候、自我介绍、解释过程、标题、原文复述或无关补充。若用户明确要求翻译，请不要使用本模板，应改用 POST /translation/。"},
    {"role": "user", "content": "<用户问题>"}
  ],
  "temperature": 0.5,
  "max_tokens": 768
}
```

`max_tokens` 依上表与 `L` 重算。**[HTTP-REQUESTS.md](./HTTP-REQUESTS.md)** · **[SKILL.md](../SKILL.md)**（`choices[0].message.content`）
