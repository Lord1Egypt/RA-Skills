---
name: youtube-summarizer
description: YouTube and Bilibili video transcript extraction and AI-powered summarization. Use when you need to summarize a YouTube or Bilibili (B站) video, extract transcripts, scan channels for new content, or generate daily video digests.
metadata:
  author: mcdowell8023
  repo: https://github.com/mcdowell8023/oc-youtube-summarizer
---

# YouTube / Bilibili Summarizer Skill

通用视频摘要工具，支持 YouTube 和 B站，支持单个视频、频道扫描、每日批量处理。

## 功能

- ✅ 获取 YouTube 视频信息（yt-dlp）
- ✅ 提取字幕/transcript（youtube-transcript-api）
- ✅ **B站视频下载 + 语音转录**（yt-dlp + faster-whisper，本地，无需 API Key）
- ✅ **B站关键帧提取**（ffmpeg，每 30 秒一帧，供 agent 视觉分析）
- ✅ 生成深度摘要（LLM API）
- ✅ 输出 JSON 格式（agent 自行处理发送）
- ✅ 支持多频道配置
- ✅ 过滤 Shorts（< 5 分钟）

## 安装

```bash
cd ~/.openclaw/skills/youtube-summarizer
./setup.sh
```

安装完成后会引导你选择默认图文模式（可随时重新配置）：

```
📋 选择默认图文模式:
  1) text-only    - 纯文字，不抽帧（最快）
  2) auto-insert  - 自动选帧插入文档（推荐平衡）
  3) ai-review    - AI 智能选图（默认，最佳效果，多消耗 ~5-8k token）
请选择 [1/2/3] (默认 3):
```

配置写入 `config/settings.json`，可随时运行 `youtube-summarizer --setup` 重新配置。

依赖：
- `yt-dlp`
- `youtube-transcript-api`
- `innertube` (绕过 YouTube 限流)
- `faster-whisper`（B站语音转录，本地，无需 API）
- `ffmpeg`（B站音频提取 + 关键帧，系统级安装）
- Python 3.9+

## 工作原理

Skill 使用多种方法获取字幕，避免 YouTube 限流：

1. **innertube ANDROID client + Cloudflare proxy** - 主要方法，绕过限流
2. **youtube-transcript-api** - 备用方法

这种双重方法确保即使 YouTube 封锁直接 API 访问也能可靠获取字幕。

## 使用

### 图文模式说明

| 模式 | 说明 | 额外 token |
|------|------|-----------|
| `text-only` | 纯文字，不抽帧 | 0 |
| `auto-insert` | 固定规则选帧，按时间戳插入（帧偏移+5s避转场） | ~0 |
| `ai-review` ← **默认** | 基于文章结构反向选图，可补帧/删帧/替换 | ~5-8k |

通过以下方式指定模式（优先级从高到低）：
1. CLI 参数 `--mode`
2. 环境变量 `SUMMARY_MODE`
3. `config/settings.json` 中的 `default_mode`

### 1. 单个视频摘要（YouTube）

```bash
youtube-summarizer --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. B站视频摘要

```bash
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx"

# 短链接也支持（自动跟随跳转）
youtube-summarizer --url "https://b23.tv/xxxxx"

# 指定图文模式
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --mode text-only
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --mode auto-insert
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --mode ai-review

# 自定义 whisper 模型（精度更高，但更慢）
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --whisper-model large-v3

# 跳过关键帧提取（等效 --mode text-only）
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --no-frames

# 自定义关键帧间隔（默认30秒一帧）
youtube-summarizer --url "https://www.bilibili.com/video/BV1xxxxx" --frame-interval 60
```

**B站处理依赖：**
- `yt-dlp` + Chrome cookies（自动读取，绕过B站反爬）
- `ffmpeg`（音频提取 + 关键帧）
- `faster-whisper`（本地语音转文字，无需API）

### 3. 频道扫描（过去 24 小时）

```bash
youtube-summarizer --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24
```

### 4. 每日批量处理（Cron 用）

```bash
youtube-summarizer --config /path/to/channels.json --daily --output /tmp/youtube_daily.json
```

## 配置文件格式

`channels.json`:
```json
{
  "channels": [
    {
      "name": "Lex Fridman",
      "id": "UCSHZKyawb77ixDdsGog4iWA",
      "url": "https://www.youtube.com/@lexfridman"
    },
    {
      "name": "Y Combinator",
      "id": "UCcefcZRL2oaA_uBNeo5UOWg",
      "url": "https://www.youtube.com/@ycombinator"
    }
  ],
  "hours_lookback": 24,
  "min_duration_seconds": 300,
  "max_videos_per_channel": 5
}
```

## 输出格式

```json
{
  "generated_at": "2026-02-14T11:17:00Z",
  "items": [
    {
      "title": "视频标题",
      "url": "https://youtube.com/watch?v=...",
      "video_id": "VIDEO_ID",
      "platform": "youtube",
      "channel": "频道名",
      "duration": "15:30",
      "published": "2026-02-14T08:00:00Z",
      "has_transcript": true,
      "summary": "# 摘要内容（markdown）\n\n### 🎯 核心问题...",
      "metadata": {
        "view_count": 12345,
        "like_count": 678
      }
    },
    {
      "video_id": "BV1xxxxx",
      "title": "B站视频标题",
      "url": "https://www.bilibili.com/video/BV1xxxxx",
      "platform": "bilibili",
      "has_transcript": true,
      "transcript_path": "/tmp/bili_BV1xxxxx_transcript.txt",
      "frame_files": ["/tmp/bili_BV1xxxxx_frames/frame_001.jpg", "..."],
      "frame_count": 12,
      "summary": "# 摘要内容（markdown）..."
    }
  ],
  "stats": {
    "total_videos": 5,
    "with_transcript": 4,
    "without_transcript": 1
  }
}
```

## Agent 使用示例

```bash
# 1. 运行 skill 生成摘要
youtube-summarizer --config youtube-channels.json --daily --output /tmp/youtube_summary.json

# 2. Agent 读取 JSON
summary=$(cat /tmp/youtube_summary.json)

# 3. Agent 处理：发送 Discord + 同步 Notion
# (在 agent prompt 或脚本中实现)
```

## Cron Job 集成

```yaml
payload:
  kind: agentTurn
  message: |
    执行 YouTube 每日摘要：
    
    1. 运行 skill:
       youtube-summarizer --config /Users/sophie/.openclaw/workspace-news/youtube-channels.json --daily --output /tmp/youtube_summary.json
    
    2. 读取 /tmp/youtube_summary.json
    
    3. 格式化并发送到 Discord (channel:1472013733122281753)
    
    4. 同步到 Notion Daily Log (3019d604-3493-812c-b86f-e156ee866612)
```

## 环境变量

| 变量 | 用途 | 必须 |
|------|------|------|
| `LLM_API_URL` | 自定义 LLM API 端点 | 否 |
| `LLM_API_KEY` | 自定义 LLM API Key | 否 |
| `LLM_MODEL` | 自定义模型名 | 否 |
| `OPENCLAW_GATEWAY_TOKEN` | OpenClaw Gateway token | 否 |
| `GITHUB_TOKEN` | GitHub token（有 Copilot 订阅时可用） | 否 |
| `POLLINATIONS_API_KEY` | Pollinations API Key | 否 |
| `SUMMARY_MODE` | 图文模式：text-only / auto-insert / ai-review | 否 |
| `WHISPER_MODEL` | B站 whisper 模型大小（默认 small） | 否 |
| `FRAME_INTERVAL` | B站关键帧间隔秒数（默认 30） | 否 |
| `FRAME_TIME_OFFSET` | 帧时间戳偏移秒数，避开转场（默认 5） | 否 |

无需任何 Key 也可运行：转录功能不需要 API Key；摘要功能会尝试 Pollinations 免费匿名调用。

## 故障排查

### 字幕获取失败
- 视频可能没有字幕
- 输出 JSON 中 `has_transcript: false`
- Agent 应生成简短摘要（基于标题/描述）

### yt-dlp 限流
- 设置 `REQUEST_DELAY_SECONDS` (默认 3 秒)
- 减少 `max_videos_per_channel`

## 与旧脚本的区别

| 旧脚本 | 新 Skill |
|--------|----------|
| 硬编码频道列表 | 配置文件驱动 |
| 直接发送 Telegram | 输出 JSON，agent 处理 |
| 单一 agent 专用 | 所有 agent 可用 |
| 逻辑耦合 | 职责分离 |
