# nanobot-feishu-send

这是一个专为 **nanobot** 设计的飞书附件发送技能。通过 nanobot 的 `message` 工具发送本地文件，**上传与消息类型自动处理**。

## 功能说明

- 发送图片、文件、语音、视频到飞书
- 支持当前会话或指定 `chat_id`
- 不需要手动调用飞书 API

## 前置条件

1. 已在 `~/.nanobot/config.json` 启用飞书渠道
2. 已运行 `nanobot gateway`
3. 文件在 **nanobot 运行的这台机器** 上

## 安装

- 通过 ClawHub 安装后，会出现在：
  `~/.nanobot/workspace/skills/nanobot-feishu-send`
- 或者把本技能文件夹放到：
  `~/.nanobot/workspace/skills/`

## 使用方法（message 工具）

**核心规则：路径必须放在 `media`，不要写到 `content`。**

### 发送图片

```json
{
  "content": "给你发图",
  "media": ["/path/to/photo.png"]
}
```

### 发送文件

```json
{
  "content": "文件已发送",
  "media": ["/path/to/report.pdf"]
}
```

### 发送语音（opus）

```json
{
  "content": "语音消息",
  "media": ["/path/to/voice.opus"]
}
```

### 发送视频

```json
{
  "content": "视频已发送",
  "media": ["/path/to/video.mp4"]
}
```

### 指定会话（可选）

```json
{
  "channel": "feishu",
  "chat_id": "ou_xxxxx",
  "content": "文件已发送",
  "media": ["/path/to/report.pdf"]
}
```

## 支持的附件类型

- 图片：`.png .jpg .jpeg .gif .bmp .webp .ico .tiff .tif`
- 语音：`.opus`
- 视频：`.mp4 .mov .avi`
- 其他：作为普通文件发送

## 常见问题

- **只发出路径文本**：路径写在 `content`，请改到 `media`
- **裂图**：文件为空/损坏/不是有效图片
- **收不到**：路径在本机不存在

## 安全建议

- 发送前确认路径与文件内容
- 妥善保管 `~/.nanobot/config.json`
