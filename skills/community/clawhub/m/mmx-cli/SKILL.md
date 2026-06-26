---
name: minimax-cli
description: MiniMax CLI (mmx) 多模态能力调用工具。当用户需要生成图片、视频、音乐、语音，或使用 minimax-cli/mmx 命令时触发。用途：(1) 生成图片/视频/音乐/语音；(2) 调用 MiniMax API；(3) 查询用量额度；(4) 配置或诊断 mmx。
---

# MiniMax CLI (mmx)

MiniMax CLI 是 MiniMax Token Plan 的命令行工具，通过 `mmx` 命令提供文本、图片、视频、语音、音乐、视觉理解、网络检索等能力。

## 安装

```bash
npm install -g mmx-cli
mmx auth login --api-key <your-api-key>
```

Agent 安装方式：将以下提示词复制给 AI Agent
```
帮我安装 MiniMax CLI：https://github.com/MiniMax-AI/cli
我的密钥是 <your-key>
```

## 全局常用选项

- `--quiet` 静默模式，减少非必要输出
- `--output json|text` 输出格式
- `--timeout <seconds>` 请求超时
- `--dry-run` 预览命令而不执行

## 图片理解

```bash
mmx vision describe --image <path-or-url> [--prompt <text>]
```

| 参数 | 说明 |
|------|------|
| `--image <path-or-url>` | 图片路径或 URL（本地路径自动 base64 编码） |
| `--file-id <id>` | 预上传的文件 ID（跳过 base64 转换） |
| `--prompt <text>` | 关于图片的问题（默认：描述图片） |

```bash
# 基础描述
mmx vision describe --image photo.jpg

# URL 图片
mmx vision describe --image https://example.com/photo.jpg

# 定制问题
mmx vision describe --image photo.jpg --prompt "这张图里有什么？"

# 提取文字
mmx vision describe --image doc.png --prompt "提取图片中的文字"

# 预上传文件（避免大文件 base64 开销）
mmx vision describe --file-id file-123456789 --prompt "这是什么？"
```

## 图片生成

```bash
mmx image generate --prompt <text> [flags]
```

| 参数 | 说明 |
|------|------|
| `--prompt <text>` | 图片描述（必填） |
| `--aspect-ratio <ratio>` | 宽高比，如 `16:9`、`1:1` |
| `--n <count>` | 生成数量（默认1） |
| `--width <px>` | 宽度（512-2048，必须是8的倍数） |
| `--height <px>` | 高度（512-2048，必须是8的倍数） |
| `--seed <n>` | 随机种子（可复现） |
| `--out <path>` | 精确保存路径（单图） |
| `--out-dir <dir>` | 保存目录 |
| `--out-prefix <prefix>` | 文件名前缀 |
| `--response-format url\|base64` | 返回格式（默认url） |
| `--prompt-optimizer` | 自动优化提示词 |
| `--aigc-watermark` | 添加AI生成水印 |
| `--subject-ref <params>` | 角色一致性参考 |

```bash
# 基础
mmx image generate --prompt "赛博朋克城市夜景" --aspect-ratio 16:9

# 批量生成到目录
mmx image generate --prompt "极简风格logo" --n 4 --out-dir ./logos/

# 精确尺寸
mmx image generate --prompt "宽屏风景" --width 1920 --height 1080

# 可复现
mmx image generate --prompt "城堡" --seed 42

# 保存路径
mmx image generate --prompt "山水画" --out ~/Pictures/landscape.jpg
```

## 视频生成

```bash
mmx video generate --prompt <text> [flags]
```

| 模型 | 说明 | 触发方式 |
|------|------|---------|
| Hailuo-2.3 (T2V) | 文本生视频（默认） | 直接使用 `--prompt` |
| Hailuo-2.3 (I2V) | 图生视频 | `--first-frame` |
| Hailuo-2.3-Fast | 快速图生视频 | `--first-frame` + fast |
| Hailuo-02 (SEF) | 首尾帧插值 | `--first-frame` + `--last-frame` |
| S2V-01 | 角色一致性 | `--subject-image` |

| 参数 | 说明 |
|------|------|
| `--prompt <text>` | 视频描述（必填） |
| `--model <model>` | 指定模型 |
| `--first-frame <path-or-url>` | 首帧图片 |
| `--last-frame <path-or-url>` | 尾帧图片（需配合 `--first-frame`） |
| `--subject-image <path-or-url>` | 角色参考图 |
| `--download <path>` | 保存路径（同步等待时） |
| `--no-wait` / `--async` | 异步模式，立即返回任务ID |
| `--poll-interval <seconds>` | 轮询间隔（默认5秒） |
| `--callback-url <url>` | 完成通知Webhook |

```bash
# 同步等待
mmx video generate --prompt "夕阳下，一只猫坐在窗边望向远方" --download sunset.mp4

# 异步，立即返回任务ID
mmx video generate --prompt "机器人画画" --async --quiet

# 图生视频
mmx video generate --prompt "一个女人在走路" --first-frame woman.jpg

# 首尾帧插值
mmx video generate --prompt "向前走" --first-frame start.jpg --last-frame end.jpg

# 角色一致性
mmx video generate --prompt "侦探行走" --subject-image character.jpg

# 查询任务状态
mmx video task get <task-id>

# 下载已完成视频
mmx video download <task-id> --out output.mp4
```

## 音乐生成

```bash
mmx music generate --prompt <text> [flags]
```

| 模型 | 说明 |
|------|------|
| music-2.6 | 推荐 |
| music-2.6-free | 免费版（无限量） |
| music-2.5+ | 增强版 |
| music-2.5 | 标准版 |

| 参数 | 说明 |
|------|------|
| `--prompt <text>` | 音乐风格描述（最多2000字符） |
| `--lyrics <text>` | 歌词（带结构标签） |
| `--lyrics-file <path>` | 从文件读取歌词 |
| `--lyrics-optimizer` | 从 prompt 自动生成歌词 |
| `--instrumental` | 纯音乐模式 |
| `--vocals <text>` | 人声风格 |
| `--genre <text>` | 音乐流派 |
| `--mood <text>` | 情绪 |
| `--instruments <text>` | 乐器 |
| `--tempo <text>` | 节奏描述 |
| `--bpm <n>` | 精确 BPM |
| `--key <text>` | 调性 |
| `--structure <text>` | 歌曲结构 |
| `--out <path>` | 保存路径（必填） |
| `--format <fmt>` | 音频格式（默认mp3） |
| `--model <model>` | 模型选择 |
| `--output-format hex\|url` | 返回格式（默认hex） |

歌词结构标签：`[Intro]` `[Verse]` `[Pre Chorus]` `[Chorus]` `[Interlude]` `[Bridge]` `[Outro]` `[Post Chorus]` `[Transition]` `[Break]` `[Hook]` `[Build Up]` `[Inst]` `[Solo]`

```bash
# 带歌词
mmx music generate --prompt "轻快爵士风格" --lyrics "La la la..." --out summer.mp3

# 自动生成歌词
mmx music generate --prompt "关于夏天的流行歌曲" --lyrics-optimizer --out summer_pop.mp3

# 纯音乐
mmx music generate --prompt "电影配乐，管弦乐" --instrumental --out bgm.mp3

# 详细参数
mmx music generate --prompt "温暖的早晨民谣" \
  --vocals "男声女声二重唱，和声" \
  --instruments "原声吉他，钢琴，弦乐" \
  --bpm 95 \
  --out duet.mp3
```

## 语音合成

```bash
mmx speech synthesize --text <text> [--out <path>] [flags]
```

| 模型 | 说明 |
|------|------|
| speech-2.8-hd | 高清（默认） |
| speech-2.6 | 标准版 |
| speech-02 | 轻量版 |

| 参数 | 说明 | 默认值 |
|------|------|-------|
| `--text <text>` | 文本（最多10k字符） | 必填 |
| `--text-file <path>` | 从文件读取 | - |
| `--voice <id>` | 音色ID | English_expressive_narrator |
| `--out <path>` | 保存路径 | - |
| `--model <model>` | 模型 | speech-2.8-hd |
| `--speed <n>` | 语速倍数 | 1.0 |
| `--pitch <n>` | 音调调整 | - |
| `--volume <n>` | 音量 | - |
| `--format <fmt>` | 音频格式 | mp3 |
| `--sample-rate <hz>` | 采样率 | 32000 |
| `--bitrate <bps>` | 比特率 | 128000 |
| `--language <code>` | 语言增强 | - |
| `--subtitles` | 包含字幕时间轴 | - |
| `--pronunciation <from/to>` | 自定义发音 | - |

查看音色列表：`mmx speech voices`

```bash
# 基础合成
mmx speech synthesize --text "欢迎使用 MiniMax Token Plan" --out welcome.mp3

# 指定音色
mmx speech synthesize --text "你好" --voice "温暖女声" --out hello.mp3

# 调整语速
mmx speech synthesize --text "快速播报新闻" --speed 1.5 --out news_fast.mp3

# 从文件读取
echo "Breaking news." | mmx speech synthesize --text-file - --out news.mp3

# 带字幕
mmx speech synthesize --text "Hello world" --subtitles --out with_subs.mp3

# 流式输出
mmx speech synthesize --text "Stream test" --stream | mpv --no-terminal -
```

## 文本对话

```bash
mmx text chat --message <text> [flags]
```

| 参数 | 说明 |
|------|------|
| `--message <text>` | 消息内容 |
| `--model <model>` | 模型选择 |
| `--stream` | 流式输出 |

```bash
# 简单对话
mmx text chat --message "帮我生成一首关于AI的4言诗"

# 流式输出
mmx text chat --message "解释量子计算" --stream
```

## 网络搜索

```bash
mmx search query <text>
```

```bash
mmx search query "MiniMax 最新动态"
```

## 其他命令

| 命令 | 说明 |
|------|------|
| `mmx auth status` | 认证状态 |
| `mmx auth refresh` | 刷新 Token |
| `mmx quota show` | 用量配额 |
| `mmx config show` | 查看配置 |
| `mmx config set <key> <value>` | 设置配置 |
| `mmx update` | 检查更新 |
| `mmx` | 打开交互面板 |

## 默认输出路径

不指定时，生成的文件默认保存到当前目录的 `minimax-output/` 文件夹。
