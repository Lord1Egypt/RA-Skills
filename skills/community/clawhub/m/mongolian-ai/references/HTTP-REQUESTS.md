# HTTP 请求示例

七种能力及异步提交均使用 HTTPS、Authorization: Bearer 与 Idempotency-Key。示例中的 ID 每个新操作必须不同；重试原请求时保留原 ID。不要在日志中打印密钥或正文。任务查询与音频下载只需 Authorization。

```sh
curl -sS -D /tmp/mongolian-response-headers \
  https://ai-skills.open-idea.net/api/v1/mongolian-ai/translation \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-translation-request-id" \
  -H "Content-Type: application/json" \
  --data '{"from":"zh","to":"mw","content":"你好"}'

curl -sS https://ai-skills.open-idea.net/api/v1/mongolian-ai/chat/completions \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-chat-request-id" \
  -H "Content-Type: application/json" \
  --data '{"messages":[{"role":"system","content":"只用西里尔蒙古文回答。"},{"role":"user","content":"介绍蒙古文化"}]}'

curl -sS https://ai-skills.open-idea.net/api/v1/mongolian-ai/tts \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-tts-request-id" \
  -H "Content-Type: application/json" \
  --data '{"text":"ᠰᠠᠢᠨ ᠪᠠᠢᠨ᠎ᠠ","lang":"mw","voice":"Kore","speed":1,"sampleRate":16000}'

curl -sS https://ai-skills.open-idea.net/api/v1/mongolian-ai/ocr \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-ocr-request-id" -F "file=@/absolute/path/image.png" -F "language=mw"

curl -sS https://ai-skills.open-idea.net/api/v1/mongolian-ai/audio \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-audio-request-id" \
  -F "file=@/absolute/path/recording.webm" -F "language=mw" -F "sample_rate=16000"

curl -sS https://ai-skills.open-idea.net/api/v1/mongolian-ai/word/translation \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-word-request-id" \
  -F "file=@/absolute/path/document.docx" -F "from=zh" -F "to=mn" -F "mode=all_text"

curl -sS https://ai-skills.open-idea.net/api/v1/mongolian-ai/pdf/translation \
  -H "Authorization: Bearer ${MONGOL_AI_SKILL_API_KEY:-$AI_SKILLS_API_KEY}" \
  -H "Idempotency-Key: unique-pdf-request-id" \
  -F "file=@/absolute/path/document.pdf" -F "from=mn" -F "to=zh" -F "mode=mongolian_only"
```

multipart 请求不要手动设置 Content-Type，让 HTTP 客户端生成 boundary。文件上传最大 5 MB，上传模式必须恰好一个 file；OCR 和 ASR 也支持互斥 Base64 输入。格式和字段详见各接口参考。读取并转述平台计费响应头，首次同步文件结果需在客户端保留，重放仅含不保留内容的状态。

长文本语音合成使用 /api/v1/mongolian-ai/tts/async（JSON，最多3000字），音频异步识别使用 /api/v1/mongolian-ai/audio/async（与同步输入相同）。202 后每3秒轮询相应 /async/{id}；completed/failed 后停止。TTS 完成后携带产品密钥下载返回的 result.audio_url。异步按提交时冻结的后台价格预留，成功仅结算一次，过期音频不能从用量历史恢复。
