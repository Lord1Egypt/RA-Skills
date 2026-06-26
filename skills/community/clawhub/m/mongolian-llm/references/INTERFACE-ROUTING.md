# 接口路由

每轮**重新**选接口。优先级：

1. 图 → `POST /ocr/`（默认 `language=mw`，西里尔 `mn`）— 细节 [OCR.md](./OCR.md)
2. 音 → `POST /audio/async/` + 轮询 `GET /audio/async/{jobId}/`；极短试 `POST /audio/` — [ASR.md](./ASR.md)
3. TTS → `POST /tts/async/`；极短试 `POST /tts/`；**禁用** `POST /tts/stream` — [TTS.md](./TTS.md)
4. 纯翻译 → `POST /translation/` — [TRANSLATION.md](./TRANSLATION.md)
5. 蒙文 + 要中文说明 → `POST /chat/completions/` 中文模板 — [CHAT-COMPLETIONS.md](./CHAT-COMPLETIONS.md)
6. 用户明确蒙文答 / 纯蒙无译词 → `POST /chat/completions/` 蒙文模板 — [CHAT-COMPLETIONS.md](./CHAT-COMPLETIONS.md)
7. Word/PDF 文档蒙文翻译 → [DOCUMENT-TRANSLATION.md](./DOCUMENT-TRANSLATION.md)

传统蒙/西里尔：无译词多 **chat**；有译词 → **translation**（如 `mw→zh`）；蒙蒙互译 → **translation** `mn↔mw`（单次）；要中文解释蒙文 → **chat** 中文模板。无蒙字：创作/介绍 → **chat**；翻译/转换 → **translation**。冲突：**给定原文要译成另一文字** → translation；**写新稿** → chat。[CHAT-COMPLETIONS.md](./CHAT-COMPLETIONS.md) · [TRANSLATION.md](./TRANSLATION.md)

**网页/长文**：净正文后 `POST /translation/`；若超过单次 `content` 上限则按 [TRANSLATION.md](./TRANSLATION.md) 分批，勿整篇用 chat 代替互译。

## OCR / ASR 衔接

OCR/ASR **成功后**只取 `data.text`；再译 → `POST /translation/`。[HTTP-REQUESTS.md](./HTTP-REQUESTS.md) · [OCR.md](./OCR.md) · [ASR.md](./ASR.md)
