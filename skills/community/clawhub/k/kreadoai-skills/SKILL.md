---
name: kreadoai
version: "1.1.0"
description: Official KreadoAI Skill. Call KreadoAI for digital avatar video generation, text-to-speech, instant avatar clone, and subtitle/watermark removal. Use subcommand account / avatar / video / clone / tts / subtitle by user intent. Use when the user mentions "KreadoAI", "Kreado", "数字人", "口播视频", "数字人视频", "文字转语音", "TTS", "形象克隆", "Avatar Clone", "字幕去除", "水印去除", "digital avatar", "talking photo", "lip sync".
metadata: {"openclaw":{"emoji":"🎭","requires":{"bins":["node"]},"primaryEnv":"KREADO_API_TOKEN","homepage":"https://www.kreadoai.com/openapi"}}
---

> **语言**：使用用户的语言进行回复。CLI 输出为中文。

# KreadoAI

数字人视频生成、文字转语音、即时形象克隆、视频字幕/水印去除。
通过子命令 `account` | `avatar` | `video` | `clone` | `tts` | `subtitle` 按用户意图调用。

## 调用方式

```bash
node skills/kreadoai/scripts/kreado.mjs <account|avatar|video|clone|tts|subtitle> [选项]
```

## 意图路由

| 用户意图 | 子命令 |
| --- | --- |
| 账户余额、VIP 状态、凭证配置 | `account` |
| 数字人形象列表、上传照片、查询上传 | `avatar` |
| 视频生成（口型同步、数字人视频） | `video` |
| 即时形象克隆（上传视频） | `clone` |
| 文字转语音（语言、声音、合成） | `tts` |
| 字幕/水印去除 | `subtitle` |

## 前置条件

- 运行环境：Node.js 18+，无需额外依赖包。
- 鉴权：环境变量 `KREADO_API_TOKEN` 或存储在 `~/.config/kreado/.credentials` 中。
- 获取 Token：https://www.kreadoai.com/ -> 账号总览 -> API 设置。

## 快速开始

```bash
node {baseDir}/scripts/kreado.mjs --help
node {baseDir}/scripts/kreado.mjs account --configure
node {baseDir}/scripts/kreado.mjs account
node {baseDir}/scripts/kreado.mjs avatar --list
node {baseDir}/scripts/kreado.mjs video --submit-system --task_name "demo" --video_ratio 2 --digital_human_id 9 --audio_url "https://..." --wait
node {baseDir}/scripts/kreado.mjs tts --languages
node {baseDir}/scripts/kreado.mjs tts --synthesize --language_id "..." --content "Hello" --voice_id "..." --voice_clone 0 --voice_source 4
node {baseDir}/scripts/kreado.mjs clone --upload --video_url "https://..." --wait
node {baseDir}/scripts/kreado.mjs subtitle --submit --task_name "test" --src_file_url "https://..." --wait
```

## 各子命令核心参数

### account
| 参数 | 用途 |
| --- | --- |
| `--info`（默认） | 查询 K-Coin 余额和 VIP 到期时间。 |
| `--configure` | 交互式输入 Token。 |
| `--import-token <token>` | 直接保存 Token。 |

### avatar
| 参数 | 说明 |
| --- | --- |
| `--list`（默认） | 列出数字人形象。`--type`, `--clone`, `--page`, `--page_size` |
| `--upload --file_url <url>` | 上传照片。`--wait` 可轮询等待。 |
| `--query --job_id <id>` | 查询上传结果。 |

### video
| 参数 | 说明 |
| --- | --- |
| `--submit-lip` | 通用视频（视频+音频）。`--task_name`, `--video_url`, `--audio_url` |
| `--submit-system` | 数字人视频。`--task_name`, `--video_ratio`, `--digital_human_id`, `--audio_url` |
| `--query --job_id <id>` | 查询结果。 |
| `--list` | 视频列表。`--page`, `--page_size`, `--status` |
| `--detail --task_id <id>` | 视频详情。 |
| `--emo-list` | 表情模板。 |

### clone
| 参数 | 说明 |
| --- | --- |
| `--upload --video_url <url>` | 上传克隆视频。`--wait` |
| `--query --job_id <id>` | 查询结果。 |

### tts
| 参数 | 说明 |
| --- | --- |
| `--languages` | 列出语言。 |
| `--voices` | 列出声音。`--language`, `--voice_clone`, `--voice_source` |
| `--synthesize` | 文字转语音。`--language_id`, `--content`, `--voice_id`, `--voice_clone`, `--voice_source` |

### subtitle
| 参数 | 说明 |
| --- | --- |
| `--submit` | 提交去除任务。`--task_name`, `--src_file_url`, `--watermark`, `--subtitle_area` |
| `--query --job_id <id>` | 查询结果。 |

## 注意事项

- 服务部署在新加坡；中国用户可能速度较慢。
- 速率限制：根据接口不同，1-60 QPS。
- K-Coin 计费：精品数字人 1/秒，臻品 2/秒，照片 1/秒，TTS 0.3/秒，字幕去除 1/秒。

## 参考

- API 文档：https://kreadoai.gitbook.io/kreadoai
- 官网：https://www.kreadoai.com/openapi
