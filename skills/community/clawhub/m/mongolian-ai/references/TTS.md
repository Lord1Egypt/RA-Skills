# 文字转语音

POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/tts

请求为 JSON，必填 `text` 与 `lang`：规范语言码支持 `mn-Cyrl`（西里尔蒙古文）、`mn-Mong`（传统蒙古文）、`zh-Hans`（中文）和 `en`（英文），并兼容 `mn`、`mw`、`zh` 别名。文本最多 600 字。可选 `voice`、`speed` 和 `sampleRate`；语速为 0.5–2，采样率支持 8000、16000、22050、44100、48000。音色支持 Kore、Puck、Zephyr、Charon、Fenrir、Aoede、Leda、Orus、Iapetus、Sulafat、Achird、Achernar。

成功返回 `data.audio_base64` 和 `data.mime_type`。客户端应严格按 `mime_type` 解码并保存为 WAV、MP3 或 OGG，不要把 Base64 文本直接展示给用户。接口按合成字符计费，必须发送唯一 `Idempotency-Key`。

文件型隐私规则同样适用于同步 TTS：成功重放只返回 `source: tts`、`replayed: true`、`content_retained: false` 和原请求编号，不再次返回音频，也不重复扣费。

异步使用 POST /api/v1/mongolian-ai/tts/async，字段与同步相同，但 text 最多 3000 字。202 返回 id/status/progress/message/request_id/billing/result，提交时预留余额，按合成字符结算。使用同一个 Idempotency-Key 重试原提交，不创建第二个付费任务。

每 3 秒 GET /api/v1/mongolian-ai/tts/async/{id}，completed/failed 后停止。完成后使用产品 Authorization 下载 result.audio_url（GET /api/v1/mongolian-ai/tts/async/{id}/audio）；此地址不是公共分享链接。音频按用户隔离，响应 private, no-store，过期返回 410；不要把密钥放到 URL。播放或下载不会重复合成或扣费。不要把任务输入或音频 Base64 写入日志。
