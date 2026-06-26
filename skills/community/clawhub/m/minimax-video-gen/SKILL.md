# MiniMax 视频生成技能

使用 MiniMax Hailuo 生成视频，支持首尾帧模式（首图→尾图）和文生视频模式。

## 功能

1. **首尾帧生成视频** - 上传首帧和尾帧图片，生成过渡视频
2. **文生视频** - 根据文本描述生成视频
3. **查询任务状态** - 查询视频生成进度
4. **下载视频** - 获取视频下载链接并下载到本地

## 前置准备

### API Key 配置
API Key 存储在 `~/.openclaw/openclaw.json` 中，路径为：
```json
{
  "models": {
    "providers": {
      "minimax-cn": {
        "apiKey": "your-api-key-here",
        "baseUrl": "https://api.minimaxi.com/anthropic"
      }
    }
  }
}
```

脚本会自动从配置文件中读取 API Key。

## 使用方式

### 首尾帧模式生成视频

```bash
cd ~/.openclaw/workspace/skills/minimax-video
node scripts/generate.js --mode fl2v \
  --first-frame "https://example.com/first.jpg" \
  --last-frame "https://example.com/last.jpg" \
  --prompt "A little girl grow up." \
  --model MiniMax-Hailuo-02 \
  --duration 6 \
  --resolution 1080P
```

### 文生视频模式

```bash
cd ~/.openclaw/workspace/skills/minimax-video
node scripts/generate.js --mode t2v \
  --prompt "A cute cat playing with a ball of yarn" \
  --model MiniMax-Hailuo-2.3 \
  --duration 6 \
  --resolution 1080P
```

### 查询任务状态

```bash
node scripts/query.js --task-id <task_id>
```

### 下载视频

```bash
node scripts/download.js --file-id <file_id> --output ./output.mp4
```

## API 文档

- **生成视频**: `POST https://api.minimaxi.com/v1/video_generation`
- **查询状态**: `GET https://api.minimaxi.com/v1/query/video_generation?task_id=xxx`
- **获取下载链接**: `GET https://api.minimaxi.com/v1/files/retrieve?file_id=xxx`

## 模型说明

| 模型 | 说明 | 推荐用途 |
|------|------|----------|
| MiniMax-Hailuo-02 | 首尾帧模式 | 图片转视频 |
| MiniMax-Hailuo-2.3 | 文生视频/图生视频 | 文字/图片生成视频 |
| MiniMax-Hailuo-2.3-Fast | 快速版本 | 快速生成 |

## 注意事项

- 下载链接有效期 **1小时**，超时需重新获取
- Token Plan 视频配额每日重置：
  - Plus-极速版: 3个/日
  - Max-极速版: 5个/日
  - Ultra-极速版: 5个/日

## 文件结构

```
minimax-video/
├── SKILL.md           # 本文档
└── scripts/
    ├── generate.js    # 生成视频主脚本
    ├── query.js       # 查询任务状态
    └── download.js    # 下载视频
```
