---
name: next-video-gen
description: 豆包 Next Video Gen AI 视频/图片生成 via 火山引擎方舟平台。支持文生图、文生视频、图生视频、素材生视频，集成 Seedance 系列模型。
homepage: https://github.com/vennduan/next-video-gen
metadata: {"requires":{"bins":["node"],"env":["DOUBAO_API_KEY"]},"primaryEnv":"DOUBAO_API_KEY"}
---

# 豆包 Next Video Gen

由 Seedance 系列模型驱动的 AI 内容生成助手，通过火山引擎方舟平台 API 工作。

## 模型

| 模型 ID | 能力 | API 端点 |
|---------|------|----------|
| `doubao-seedream-5-0-260128` | 文生图 | `POST /v3/images/generations` |
| `doubao-seedance-1-5-pro-251215` | 文生视频、图生视频、素材生视频（1.5 Pro） | `POST /v3/contents/generations/tasks` |
| `doubao-seedance-2-0-260128` | 文生视频、图生视频、素材生视频（2.0） | `POST /v3/contents/generations/tasks` |

**默认模型**: `doubao-seedance-1-5-pro-251215`

## 生成模式

| 模式 | 说明 | 必需参数 |
|------|------|---------|
| `txt2img` | 文生图 | prompt |
| `txt2video` | 文生视频（默认无音频） | prompt, duration |
| `img2video` | 图生视频 | prompt, image URL, duration |
| `vid2video` | 素材生视频 | prompt, video URL, duration |

### 字幕处理

当前 API 暂无独立的字幕参数。如需字幕，可将字幕内容写入 prompt 中描述（如「底部有白色字幕：xxx」），模型会根据描述自行处理。此方式非原生支持，效果取决于模型理解能力。

## 参数说明

### 图片参数（txt2img）

| 参数 | 默认值 | 可选值 | 说明 |
|------|--------|--------|------|
| `--quality` | `2K` | `2K`, `1K`, `HD` | 分辨率。2K ≈ 2048px |
| `--aspect-ratio` | `1:1` | `1:1`, `16:9`, `9:16` | 宽高比 |
| `--watermark` | `true` | `true`, `false` | 是否显示水印 |

### 视频参数（txt2video / img2video / vid2video）

| 参数 | 默认值 | 可选值 | 说明 |
|------|--------|--------|------|
| `--duration` | `5` | `4`–`12` | 时长（秒） |
| `--quality` | `720p` | `480p`, `720p`, `1080p` | 分辨率 |
| `--aspect-ratio` | `16:9` | `16:9`, `9:16`, `1:1` | 宽高比 |
| `--watermark` | `true` | `true`, `false` | 是否显示水印 |
| `--enable-audio` | — | — | 启用音频（视频默认无音频） |
| `--model` | `doubao-seedance-1-5-pro-251215` | 见模型表 | 指定模型 |

### 参考素材

| 参数 | 说明 |
|------|------|
| `--image <url>` | 参考图片（图生视频），可多次使用多张 |
| `--video <url>` | 视频素材（素材生视频） |
| `--audio <url>` | 参考音频（作为背景音乐） |

## 用法

### Node.js 脚本（推荐，跨平台）

```bash
# 设置 API key
export DOUBAO_API_KEY=your_key_here

# 文生图
node scripts/run-gen.js "一只橘猫在阳光下打盹" --mode txt2img

# 文生图（指定分辨率和比例）
node scripts/run-gen.js "未来城市夜景" --mode txt2img --quality 2K --aspect-ratio 16:9

# 文生视频（默认无音频）
node scripts/run-gen.js "海上日落延时摄影" --mode txt2video

# 文生视频（带音频）
node scripts/run-gen.js "海上日落延时摄影，海浪轻拍" --mode txt2video --audio

# 图生视频
node scripts/run-gen.js "镜头缓慢推进，猫咪转身" --mode img2video --image "https://example.com/cat.jpg"

# 多张参考图生视频
node scripts/run-gen.js "从第一张平滑过渡到第二张" --mode img2video --image "https://example.com/1.jpg" --image "https://example.com/2.jpg"

# 素材生视频
node scripts/run-gen.js "镜头加快，色彩更鲜艳" --mode vid2video --video "https://example.com/input.mp4"

# 素材生视频 + 参考音频
node scripts/run-gen.js "节奏加快，配欢快背景音乐" --mode vid2video --video "https://example.com/input.mp4" --audio "https://example.com/bgm.mp3"

# 指定模型（2.0）
node scripts/run-gen.js "无人机航拍山谷" --mode txt2video --model doubao-seedance-2-0-260128 --duration 8 --quality 1080p

# 竖屏视频
node scripts/run-gen.js "瀑布流淌" --mode txt2video --aspect-ratio 9:16

# 关闭水印
node scripts/run-gen.js "抽象艺术动画" --mode txt2video --watermark false
```

### Bash 脚本（旧版，兼容）

```bash
./scripts/seedance-gen.sh "小猫在草地上奔跑" --mode txt2video
```

**依赖**: node（无 jq，无 curl）

**输出目录**: `~/Videos/next-video-gen/`（可通过环境变量 `NEXT_VIDEO_GEN_OUTPUT_DIR` 配置）

## 脚本输出协议

解析以下结构化行并处理：

| 行格式 | 何时出现 | 操作 |
|--------|---------|------|
| `TASK_SUBMITTED: task_id=<id> mode=<模式>` | 提交后 | 告诉用户任务已开始 |
| `STATUS_UPDATE: <message>` | 每 30 秒 | 告诉用户进度 |
| `IMAGE_URL=<url>` | 图片成功 | 展示 URL（链接短期有效，及时下载） |
| `VIDEO_URL=<url>` | 视频成功 | 展示 URL（链接短期有效，及时下载） |
| `ELAPSED=<Ns>` | 成功时 | 可提及耗时 |
| `DURATION=<Xs>` | 视频成功 | 展示时长 |
| `ASPECT_RATIO=<ratio>` | 成功时 | 展示比例 |
| `RESOLUTION=<res>` | 成功时 | 展示分辨率 |
| `HAS_AUDIO=<true\|false>` | 视频成功 | true 时告知"含音频" |
| `LOCAL_FILE=<path>` | 成功时 | 告知本地保存路径 |
| `ERROR: ...` | 失败时 | 展示错误信息 |

## 交付标准

生成成功后，完整呈现：

**① 本地文件** — 告知保存路径
**② 规格** — 分辨率、宽高比、时长、是否含音频
**③ 在线链接** — 注明「链接有时效，及时下载」
**④ 耗时** — 可选

示例（视频）：
```
✅ 视频生成完成！

📁 本地文件：~/Videos/next-video-gen/video_20240412_153012.mp4
🎬 规格：5秒 · 720p · 16:9 · 无音频
🔗 在线链接（请尽快下载，短期内有效）：<VIDEO_URL>
⏱ 生成用时：47秒
```

示例（图片）：
```
✅ 图片生成完成！

📁 本地文件：~/Videos/next-video-gen/img_20240412_153012.png
🖼 规格：2K · 1:1
🔗 在线链接（请尽快下载，短期内有效）：<IMAGE_URL>
⏱ 生成用时：8秒
```

> 注意：在线链接含临时签名，24 小时内有效，过期后需重新生成。

## 错误处理

| 错误码 | 说明 | 用户操作 |
|--------|------|---------|
| `401` | API Key 无效 | 去控制台检查密钥 |
| `403` | 权限不足 | 检查密钥的模型权限 |
| `429` | 请求过频 | 稍后重试 |
| `500`-`503` | 服务异常 | 稍后重试 |
| `HTTP_ERROR:Client network socket disconnected` | Windows 环境 HTTPS 问题 | 重试，通常第二次成功 |

## 安装后

技能首次加载时检查 `DOUBAO_API_KEY`：
- **已设置**: "准备好了！你想生成什么？"
- **未设置**: "需要配置豆包 API 密钥才能使用。去火山引擎控制台获取一下吗？" 并引导配置。

## 核心原则

1. **引导而非替用户决定** — 提供选项，让用户自己选
2. **用户驱动创意** — 用用户的描述，需要时提供建议
3. **智能上下文感知** — 只询问缺失部分
4. **意图优先** — 意图不明确时先确认

---

## 参考

- 文生图模型: https://console.volcengine.com/ark/model_detail?Id=doubao-seedream-5-0-260128
- 视频 1.5 Pro: https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-1-5-pro-251215
- 视频 2.0: https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-2-0-260128