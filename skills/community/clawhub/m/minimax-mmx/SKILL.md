---
name: minimax-mmx
description: MiniMax MMX-CLI 命令行工具，用于 AI Agent 调用 MiniMax 全模态能力（图片生成、视频生成、语音合成、音乐创作、图片理解、网络搜索、文本对话等）。当用户需要生成图片、视频、语音旁白、音乐，或者需要理解图片内容、执行搜索时使用此技能。安装：npm install -g mmx-cli；鉴权：mmx auth login --api-key <key>
---

# MMX-CLI - MiniMax 全模态命令行工具

## 快速开始

```bash
# 鉴权（如未配置）
mmx auth login --api-key <your-api-key>

# 查看配额
mmx quota show
```

## 核心命令

### 图片生成 (image-01)
```bash
mmx image generate --prompt "描述" --aspect-ratio 16:9 --out-dir ./output --quiet --output json
```
- `--n`: 生成数量 (1-4)
- `--subject-ref`: 角色一致性参考

### 语音合成 (speech-hd)
```bash
mmx speech synthesize --text "文本" --voice "中文主播" --out audio.mp3 --quiet --output json
```
- 查看可用声音：`mmx speech voices`

### 音乐创作 (music-2.5)
```bash
mmx music generate --prompt "描述" --out music.mp3 --quiet --output json
```

### 视频生成 (MiniMax-Hailuo-2.3)
```bash
# 同步（等待完成）
mmx video generate --prompt "描述" --out video.mp4 --duration 6

# 异步（不阻塞）
mmx video generate --prompt "描述" --out video.mp4 --async
mmx video task get <task-id>  # 查询状态
mmx video download <task-id>   # 下载
```

### 图片理解
```bash
mmx vision describe --image path/to/image.jpg --quiet --output json
```

### 网络搜索
```bash
mmx search query --query "关键词" --quiet --output json
```

### 文本对话
```bash
mmx text chat --prompt "问题" --quiet --output json
```

## Agent 优化参数

| 参数 | 作用 |
|------|------|
| `--quiet` | 抑制进度条、彩色字符，只输出结果 |
| `--output json` | 输出纯 JSON，避免解析干扰 |
| `--async` | 异步模式，长任务转后台执行 |
| `--non-interactive` | 禁用交互式提示，CI/Agent 模式 |

## 错误处理（Exit Codes）

| Code | 含义 | 处理 |
|------|------|------|
| 0 | 成功 | - |
| 1 | 通用错误 | 查看 error.message |
| 401 | 鉴权失败 | 重新 `mmx auth login` |
| 400 | 参数错误 | 检查命令参数 |
| 408 | 请求超时 | 重试 |
| 429 | 速率限制 | 等待后重试 |

详细命令参考：See [references/commands.md](references/commands.md)
