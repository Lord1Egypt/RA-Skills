# 渠道原生文件发送参考

> 本文档包含各消息渠道文件发送的详细技术原理。SKILL.md 中按需引用。

---

## 通用机制：MEDIA: 行

OpenClaw **核心 deliver 引擎**统一处理 `MEDIA:` 行（适用于所有渠道）：

```
Agent 回复包含 MEDIA: /tmp/openclaw/nas-courier/file.pdf
  ↓ 核心 splitMediaFromOutput() 解析 MEDIA: 行
  ↓ normalizeReplyPayloadsForDelivery() 合并 mediaUrls
  ↓ deliver 引擎遍历 mediaUrls → 调用渠道 handler.sendMedia(caption, url)
```

**MEDIA: 行格式**:
```
MEDIA: /tmp/openclaw/nas-courier/2025年报.pdf          # 本地路径（推荐）
MEDIA: https://example.com/file.pdf           # HTTP URL
MEDIA: "/tmp/openclaw/nas-courier/文件 带空格.pdf"     # 带引号处理空格
```

---

## 飞书 (feishu-china) — ✅ 已验证

### 发送方式

```
# 方式 1（推荐）: MEDIA: 前缀行
MEDIA: /tmp/openclaw/nas-courier/2025年报.pdf

# 方式 2: 裸路径（outbound 也能自动识别）
/tmp/openclaw/nas-courier/2025年报.pdf

# 方式 3: Markdown 链接
[2025年报.pdf](/tmp/openclaw/nas-courier/2025年报.pdf)
```

### 技术原理

```
MEDIA: /tmp/openclaw/nas-courier/file.pdf
  ↓ extractMediaLinesFromText() 提取 MEDIA: 行
  ↓ 判断扩展名：图片 → sendImageFeishu / 其他 → sendFileFeishu
  ↓ sendFileFeishu:
      1. readLocalFileStream() 读取本地文件
      2. uploadFeishuFile() → POST /open-apis/im/v1/files (获取 file_key)
      3. im.v1.message.create({ msg_type: "file", content: { file_key } })
  ↓ 文件直接出现在飞书聊天中（用户可直接下载）
```

### 飞书文件类型映射

| 扩展名 | 飞书 file_type |
|--------|---------------|
| .opus | opus |
| .mp4 .mov .m4v .avi .mkv .webm | mp4 |
| .pdf | pdf |
| .doc .docx .rtf .odt | doc |
| .xls .xlsx .csv .ods | xls |
| .ppt .pptx | ppt |
| 其他 | stream |

> 图片文件 (.jpg .png .gif .webp .svg) 通过 `sendImageFeishu` → `im/v1/images` 以图片消息发送。

---

## Telegram — ✅ 已验证

### 发送方式

```
# 与飞书相同：
MEDIA: /tmp/openclaw/nas-courier/2025年报.pdf
```

### 技术原理

```
MEDIA: /tmp/openclaw/nas-courier/file.pdf
  ↓ 核心 splitMediaFromOutput() 解析（所有渠道共用）
  ↓ deliver 引擎调用 handler.sendMedia(caption, mediaUrl)
  ↓ Telegram loadWebMedia() 加载本地文件
  ↓ kindFromMime() 判断类型 → 选择 Bot API 方法：
      图片 → sendPhoto    | 视频 → sendVideo
      音频 → sendAudio    | GIF  → sendAnimation
      语音 → sendVoice    | 其他 → sendDocument（默认）
  ↓ 文件直接出现在 Telegram 聊天中
```

### Telegram 文件大小限制

- **上传** (Bot → 用户): 最大 50MB
- **下载** (用户 → Bot): 最大 20MB
- 超出限制 → 使用 HTTP 临时下载链接方案（见 http-temp-link.md）

---

## QQ Bot (openclaw-qqbot) — ✅ 已验证

### 发送方式

```
# 与飞书/Telegram 相同：
MEDIA: /tmp/openclaw/nas-courier/2025年报.pdf
```

### 技术原理

```
MEDIA: /tmp/openclaw/nas-courier/file.pdf
  ↓ 核心 splitMediaFromOutput() 解析（所有渠道共用）
  ↓ deliver 引擎调用 handler.sendMedia(caption, mediaUrl)
  ↓ qqbotOutbound.sendMedia()
  ↓ sendFileQQBot():
      1. resolveQQBotMediaFileType() 判断文件类型
      2. readMediaWithConfig() 读取本地文件到 buffer
      3. uploadQQBotFile() → POST /v2/users/{openid}/files 或 /v2/groups/{groupid}/files
      4. sendC2CMediaMessage / sendGroupMediaMessage → POST /v2/.../messages
  ↓ 文件直接出现在 QQ 聊天中
```

### QQ Bot 文件类型映射

| 类型 | file_type 值 | 说明 |
|------|-------------|------|
| 图片 (.jpg .png .gif .webp .bmp) | 1 (IMAGE) | 以图片消息发送 |
| 视频 (.mp4 .mov .avi .mkv .webm) | 2 (VIDEO) | 以视频消息发送 |
| 音频 (.mp3 .wav .ogg .opus .silk) | 3 (VOICE) | 音频自动转 silk 格式 |
| 其他 | 4 (FILE) | 以文件消息发送（默认） |

### QQ Bot 限制

- **文件大小**: 默认最大 100MB（可通过 `maxFileSizeMB` 配置）
- **语音**: 自动转换为 silk 格式（QQ 要求）
- **主动发送**: CLI `openclaw message send --channel qqbot` 存在参数映射 bug，但 agent 回复中的 MEDIA: 行通过 deliver 引擎正常工作
