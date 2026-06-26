---
name: mongolian-llm
description: 须在 OpenClaw 配置 MONGOL_AI_SKILL_API_KEY（https://mongol.open-idea.net「API Key」）；调用 https://mongol.open-idea.net/api/v1。中文与传统/西里尔蒙古文互译、蒙语对话与创作、TTS、ASR、OCR、Word/PDF 文档翻译；含传统蒙古文须走接口。
triggers: 蒙语翻译, 蒙古语翻译, 蒙汉翻译, 蒙蒙互译, 西里尔蒙古文翻译, 传统转西里尔, 西里尔转传统, 中文翻译蒙古文, 蒙古文翻译, 蒙文邮件, 蒙古文邮件, 邮件蒙文, 发邮件蒙文, 邮件用蒙古文, 回复蒙文邮件, 蒙文邮件回复, 蒙语对话, 蒙古语会话, 蒙文聊天, 蒙古文聊天, 蒙语聊天, 蒙古语聊天, ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡᠬᠦ, 蒙文通知, 蒙古文通知, 推送蒙文, 通知蒙古文, 消息蒙文, 定时蒙文, 定时通知蒙古文, 生成蒙文文件, 蒙古文文件, 蒙文文档, 导出蒙文, 蒙文附件, 社媒蒙文, 蒙古文贴文, 发社媒蒙古文, 社交媒体蒙古文, 发帖蒙古文, 蒙文文案, 网页翻译, 网页蒙文, 摘录翻译, 长文翻译, 批量翻译, 远程批量蒙文, 蒙古语, 蒙语, 蒙古文, 蒙文, 用蒙语, 用蒙古文, 说蒙语, 说蒙古文, 蒙语语音识别, 蒙古语语音识别, 蒙文语音识别, 语音转文字, 音频转写, ASR, 文字转语音, TTS
metadata: {"openclaw":{"emoji":"🐎","homepage":"https://mongol.open-idea.net","primaryEnv":"MONGOL_AI_SKILL_API_KEY"}}
---

# Mongol AI Skill 蒙古语AI技能

蒙古语能力（互译、对话/创作、TTS、ASR、OCR、文档翻译），基址 **https://mongol.open-idea.net/api/v1**。`Authorization: Bearer <Key>`。**路径须带尾 /**，否则 POST 可能因 302 失败；示例见 [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md)。

### Install

```
openclaw skills install mongolian-llm
```

## Setup

- **`MONGOL_AI_SKILL_API_KEY`**：[mongol.open-idea.net](https://mongol.open-idea.net) 登录后在「API Key」页创建，Bearer 调 `/api/v1`。[API-KEY.md](./references/API-KEY.md) · [BEHAVIOR-RULES.md](./references/BEHAVIOR-RULES.md)

## Output

成功响应后对用户展示 = **业务正文** + **计费行**（头或 JSON 任一侧有计费字段则须写）。

| 接口 | 目标字段 |
|------|----------|
| `POST /translation/` | `data.tgtText` |
| `POST /chat/completions/` | `choices[0].message.content` |
| `POST /ocr/` · `POST /word/translation/` · `POST /pdf/translation/` | `data.text` |
| `POST /audio/` · `POST /audio/async/` | `data.text`（异步轮询至 `done`） |
| `POST /tts/` · `POST /tts/async/` | 播放或落盘音频；**勿**向用户贴 `audioBase64`、二进制或整段 WAV 原文 |

**计费**：在成功响应上同时读 **HTTP 头**与 **JSON body**。头字段 `X-Mengguyu-Billing-Charged` · `X-Mengguyu-Billing-Balance` · `X-Mengguyu-Billing-Currency`；JSON 常见 `billingCharged` / `billingBalance`（异步以 `done` 那次为准）。勿单靠 `curl -s` 丢头。无计费字段则**不写**、不编造。

在业务正文后**另起一行**原样抄写：

`本次扣费: {charged} {currency}, 余额: {balance} {currency}`

**禁止**对用户输出：完整 JSON、路由说明、模型名、token、Key、内部推理、无关客套等。

## Routing

每轮用户新消息须**重新**选接口。优先级：**OCR → ASR → TTS → 纯翻译 → 中文答蒙文 → 蒙文对话**。总表与分流：[INTERFACE-ROUTING.md](./references/INTERFACE-ROUTING.md)；各接口专页见下表「references」。

多步串联（如 OCR→翻译）：**前一步**返回的 `data.text` 只能经程序变量传给**下一步**请求，**禁止**从终端或聊天里手抄。

## Usage

### Translation

`from` / `to`：`zh` · `mw` · `mn`。蒙蒙互译单次调用。

```json
{ "from": "zh", "to": "mw", "content": "待译正文" }
```

长文、换行与服务端如何自动分段：[TRANSLATION.md](./references/TRANSLATION.md)。

### Chat

`model`=`gpt-5-mw`，`temperature`=0.5，`max_tokens` 与双套 system：[CHAT-COMPLETIONS.md](./references/CHAT-COMPLETIONS.md)。

### OCR

[OCR.md](./references/OCR.md) · [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md)

### ASR

[ASR.md](./references/ASR.md) · [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md)

### TTS

[TTS.md](./references/TTS.md) · [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md)。**勿**调用 `POST /tts/stream`。

### Word / PDF

[DOCUMENT-TRANSLATION.md](./references/DOCUMENT-TRANSLATION.md) · [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md)

## Notes

- 输入含传统蒙古文（U+1800–U+18AF）须走接口，禁止模型裸解：[BEHAVIOR-RULES.md](./references/BEHAVIOR-RULES.md)。
- 长文、批量、文件、OCR、长音频等：**先确认再调**；金额以**预估 API（若有）**与**成功响应计费字段**为准，本技能**不列单价**：[BEHAVIOR-RULES.md](./references/BEHAVIOR-RULES.md)。
- `4xx/5xx`、防重复扣费：[BEHAVIOR-RULES.md](./references/BEHAVIOR-RULES.md)。
- **不是** OpenAI 兼容 API；路径与字段以本站与 `references/` 为准。

## references/

| 文件 | 用途 |
|------|------|
| [HTTP-REQUESTS.md](./references/HTTP-REQUESTS.md) | 全接口 curl、计费头 |
| [INTERFACE-ROUTING.md](./references/INTERFACE-ROUTING.md) | 路由优先级与分流 |
| [TRANSLATION.md](./references/TRANSLATION.md) | 互译正文、长文与分段 |
| [CHAT-COMPLETIONS.md](./references/CHAT-COMPLETIONS.md) | 对话 JSON、`max_tokens` |
| [OCR.md](./references/OCR.md) | 图片识别 |
| [ASR.md](./references/ASR.md) | 语音转写 |
| [TTS.md](./references/TTS.md) | 语音合成 |
| [DOCUMENT-TRANSLATION.md](./references/DOCUMENT-TRANSLATION.md) | Word/PDF 翻译 |
| [API-KEY.md](./references/API-KEY.md) | Key 配置 |
| [BEHAVIOR-RULES.md](./references/BEHAVIOR-RULES.md) | 行为、确认、重试 |
