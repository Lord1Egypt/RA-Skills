# 语音识别

POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/audio

文件使用 multipart/form-data，最大 5 MB，支持 WAV/MP3/M4A/AAC/OGG/FLAC/PCM/WebM。也可使用 JSON 提交 pcm_base64（兼容 audio_base64 别名）；与 file 互斥且不得同时提供两种 Base64 字段。PCM 为单声道 16-bit little-endian，解码后最大 5 MB，不带 Data URL 前缀。language 必填，支持 mw/mn/zh/en；sample_rate 可选，默认 16000，允许 8000、16000、48000。

成功只提取 data.text。停止录音不会提交付费识别请求；用户明确点击或确认开始识别后才发送。若用户还要翻译，再使用新的幂等键请求 /translation。重放没有转写正文。

异步使用 POST /api/v1/mongolian-ai/audio/async，输入与同步相同，使用稳定 Idempotency-Key。202 返回 id/status/progress/message/request_id/billing/result；此时仅预留余额。每 3 秒 GET /api/v1/mongolian-ai/audio/async/{id}，终态 completed/failed 后停止；completed 时读取 result.text。查询必须使用同产品密钥，任务按用户隔离。长音频由平台按 22 秒 PCM 顺序分片并合并，只结算一次；最长必须小于 328 秒。轮询不产生新识别或重复扣费；结果过期时不可重试创建付费任务，先通知用户。结果不确定或已有分片成功后失败时保留预留用于对账。
