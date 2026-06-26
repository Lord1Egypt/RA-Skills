---
name: nanobot-feishu-send
description: 用 nanobot 的 message 工具向飞书发送图片/文件/语音/视频，上传与消息类型自动处理。
---

# nanobot 飞书发送（nanobot-feishu-send）

这是为 **nanobot** 设计的飞书附件发送技能。**唯一正确方式**是通过 `message` 工具传本地文件路径到 `media`。

## 适用场景

- 给飞书发送图片、文件、语音、视频
- 需要把本机文件作为附件发到当前飞书会话

## 前置条件

- `~/.nanobot/config.json` 已启用飞书渠道
- nanobot 网关已运行：`nanobot gateway`
- 附件文件存在于 **nanobot 运行的这台机器**

## 正确用法（必须遵守）

**核心规则**：文件路径必须放在 `media`，路径不要写在 `content`。

### 发送流程

1. 确认路径是本机路径且文件存在
2. 把路径放进 `media`
3. 调用 `message` 工具发送

### 正确示例（直接复制）

发送图片：

```json
{
  "content": "给你发图",
  "media": ["/path/to/photo.png"]
}
```

发送文件：

```json
{
  "content": "文件已发送",
  "media": ["/path/to/report.pdf"]
}
```

发送语音（推荐 opus）：

```json
{
  "content": "语音消息",
  "media": ["/path/to/voice.opus"]
}
```

发送视频：

```json
{
  "content": "视频已发送",
  "media": ["/path/to/video.mp4"]
}
```

指定会话（可选）：

```json
{
  "channel": "feishu",
  "chat_id": "ou_xxxxx",
  "content": "文件已发送",
  "media": ["/path/to/report.pdf"]
}
```

## 错误示例（会只发路径）

```json
{
  "content": "/path/to/photo.png"
}
```

## 支持的附件类型

- **图片**：`.png .jpg .jpeg .gif .bmp .webp .ico .tiff .tif`
- **语音**：`.opus`
- **视频**：`.mp4 .mov .avi`
- **其他文件**：发送为普通文件

## 快速自检（避免裂图）

发送前检查：

1. 文件路径存在（不是 URL）
2. 文件大小 > 0，且确实是图片/文件
3. 路径只在 `media` 中

如果用户给的是 URL：先下载到本机，再用本地路径发送。

## 常见问题

- **只发出路径文本**：路径写在了 `content`，请改为 `media`。
- **裂图**：文件损坏/空文件/不是图片但扩展名伪装。
- **语音没显示为语音**：请使用 `.opus`。
