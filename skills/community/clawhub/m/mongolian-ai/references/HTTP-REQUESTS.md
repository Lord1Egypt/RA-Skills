# HTTPS 请求模板

路径**须**带尾 `/`（否则 POST 可能 302 失败）。输出与计费句式：[SKILL.md](../SKILL.md)。

```text
https://mongol.open-idea.net/api/v1
```

```http
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
Content-Type: application/json
```

**计费头**（异步亦可能在 JSON：`billingCharged` / `billingBalance`）：

```http
X-Mengguyu-Billing-Currency: CNY
X-Mengguyu-Billing-Charged: <本次扣费>
X-Mengguyu-Billing-Balance: <当前余额>
```

读头 + body；勿单靠 `curl -s`。multipart `file` 约 **≤10 MB**（JSON PCM Base64 解码后同量级）。

---

## `POST /translation/`

正文规则 [TRANSLATION.md](./TRANSLATION.md)。

```http
POST /translation/ HTTP/1.1
Host: mongol.open-idea.net
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
Content-Type: application/json
```

```json
{ "from": "zh", "to": "mw", "content": "你好朋友" }
```

→ `data.tgtText`（细则 [TRANSLATION.md](./TRANSLATION.md)）。

---

## `POST /chat/completions/`

模板与 `max_tokens` [CHAT-COMPLETIONS.md](./CHAT-COMPLETIONS.md)。示例 `max_tokens:768` 对应 `L`∈51～200。

```http
POST /chat/completions/ HTTP/1.1
Host: mongol.open-idea.net
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
Content-Type: application/json
```

```json
{
  "model": "gpt-5-mw",
  "messages": [
    {"role": "system", "content": "请只用纯传统蒙古文回答，不要包含任何中文汉字。"},
    {"role": "user", "content": "用户问题或创作要求"}
  ],
  "temperature": 0.5,
  "max_tokens": 768
}
```

中文 `system`、`L` 重算：**[CHAT-COMPLETIONS.md](./CHAT-COMPLETIONS.md)**。→ `choices[0].message.content`。

---

## `POST /ocr/`

要点 [OCR.md](./OCR.md)。

```http
POST /ocr/ HTTP/1.1
Host: mongol.open-idea.net
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
Content-Type: application/json
```

```json
{
  "image_base64": "<Base64>",
  "language": "mw",
  "image_encoding": "jpg"
}
```

→ `data.text`。`jpg|png|bmp|webp|tif|tiff|gif`。

---

## `POST /audio/`（同步）

要点 [ASR.md](./ASR.md)。

multipart：`POST /audio/`，`language` · `sample_rate` · `file`。

```http
POST /audio/ HTTP/1.1
Host: mongol.open-idea.net
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
Content-Type: multipart/form-data; boundary=<boundary>
```

JSON PCM Base64：

```json
{ "audio": "<PCM16 mono B64>", "language": "mw", "sample_rate": 16000 }
```

→ `data.text`

### `POST /audio/async/`

`POST` → **202** + `jobId`；**3～5s** `GET /audio/async/{jobId}/` 至 **200** + `data.text`（**202**=processing，**422**=failed）。可选 `DELETE /audio/async/{jobId}/`。

---

## TTS

音色与调用约定 [TTS.md](./TTS.md)。长文异步；上游约每 **200** 蒙文自动并段。

### `POST /tts/async/`

```http
POST /tts/async/ HTTP/1.1
Host: mongol.open-idea.net
Authorization: Bearer <MONGOL_AI_SKILL_API_KEY>
Content-Type: application/json
```

```json
{ "text": "<待合成>", "lang": "mn-Mong", "voice": "Kore" }
```

→ **202** + `jobId`；轮询 `GET /tts/async/{jobId}/` 至 **200**、`status:done`，`audioBase64` → WAV。**422**=failed。计费 [SKILL.md](../SKILL.md)。**勿**用 `POST /tts/stream`。

`lang`：`mn-Mong` `mn-Cyrl` `zh-Hans` `en` `ja` `ko` `ru`；`voice` [TTS.md](./TTS.md)；`speed` 0.5～2.0。

---

## `POST /word/translation/` · `POST /pdf/translation/`

细节 [DOCUMENT-TRANSLATION.md](./DOCUMENT-TRANSLATION.md)。multipart：`from` · `to` · `mode`（如 `mongolian_only`）· `file` → `data.text`。
