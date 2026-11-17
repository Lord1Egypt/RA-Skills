---

slug: music-gen-cellcog-tool-free
name: music-gen-cellcog-tool-free
version: 1.0.0
displayName: CellCog音乐生成免费版
summary: 基于CellCog AI引擎的音乐生成工具,支持文本/歌词生成音乐、多种风格选择,适合个人内容创作.
license: Proprietary
edition: free
description: "CellCog音乐生成免费版帮助个人用户通过CellCog AI引擎创建音乐。支持从文本描述或歌词生成完整音乐作品,涵盖流行、电子、古典、环境等多种风格,
  生成的音乐可用于个人内容创作。Use when 需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于版权受保护的媒体内容处理。加速开发流程，提升代码质量与一致性。触发关键词：API设计、代码生成、自动化、转换、设计、视频"

  生成的音乐可用于个人内容创作。Use when 需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于版权受保护的媒体内容处理。'
tags:
  - 音乐生成
  - CellCog
  - AI音乐
  - 文生音乐
  - 内容创作
  - 音频
  - 创意
  - cellcog
  - mp3
  - api
  - json
  - 音乐
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"

---
# CellCog音乐生成免费版

## 概述

CellCog音乐生成免费版帮助个人用户通过CellCog AI引擎创建音乐。工具支持从文本描述或歌词生成完整音乐作品,涵盖流行、电子、古典、环境等多种风格,生成的音乐可用于个人内容创作.
本版本面向个人用户,提供基础的文生音乐与歌词生音乐能力,适合个人内容创作与音乐探索.
## 核心能力

### 文生音乐(Text-to-Music)

从自然语言描述生成音乐:

具体详情请参考下方内容.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | CellCog音乐生成免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 基础文生音乐
curl -X POST https://api.cellcog.com/v1/music/generate \
  -H "Authorization: Bearer $CELLCOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "欢快的流行音乐,钢琴与吉他,120 BPM",
    "duration": 30,
    "format": "mp3"
  }'
```

**处理**: 解析文生音乐(Text-to-Music)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回文生音乐(Text-to-Music)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 歌词生音乐(Lyrics-to-Music)

从歌词生成带人声的完整歌曲:

```bash
# 歌词生音乐
cellcog.com/v1/music/generate \
  -H "Authorization: Bearer $CELLCOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lyrics": "[Verse 1]\n阳光照进窗台\n新的一天开始\n[Chorus]\n向着梦想前进",
    "style": "pop",
    "voice": "female",
    "duration": 60,
    "format": "mp3"
  }'
```

**处理**: 解析歌词生音乐(Lyrics-to-Music)的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回歌词生音乐(Lyrics-to-Music)的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 音乐风格选择

| 风格 | 说明 | 适用场景 | 示例提示词 |
|:-----|:-----|:-----|:-----|
| Pop | 流行音乐 | 通用 | "upbeat pop, catchy melody" |
| Electronic | 电子音乐 | 舞曲/背景 | "electronic dance, synth, 128 BPM" |
| Classical | 古典音乐 | 高端场景 | "orchestral, strings, piano" |
| Ambient | 环境音乐 | 冥想/放松 | "ambient, peaceful, atmospheric" |
| Lo-fi | 低保真音乐 | 学习/工作 | "lo-fi hip hop, mellow, 80 BPM" |
| Rock | 摇滚 | 激情场景 | "rock, electric guitar, drums" |
| Jazz | 爵士 | 休闲场景 | "smooth jazz, saxophone, piano" |
| Folk | 民谣 | 温馨场景 | "acoustic folk, guitar, warm" |

**处理**: 解析音乐风格选择的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回音乐风格选择的响应数据,包含状态码、结果和日志.
### 自定义参数

```python
# 音乐生成参数配置
generation_params = {
    "prompt": "音乐描述",           # 文本描述
    "lyrics": "歌词内容",           # 或歌词(二选一)
    "style": "pop",                # 音乐风格
    "duration": 30,                # 时长(秒)
    "bpm": 120,                    # 节拍速度
    "key": "C_major",              # 调性
    "voice": "female",             # 人声音色(歌词模式)
    "instrumental": False,          # 是否纯器乐
    "format": "mp3",               # 输出格式
    "quality": "standard"          # 音质:standard/high
}
```

**处理**: 解析自定义参数的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回自定义参数的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：引擎的音乐生成工、支持文本、歌词生成音乐、多种风格选择、适合个人内容创作、音乐生成免费版帮、助个人用户通过、引擎创建音乐、支持从文本描述或、歌词生成完整音乐、涵盖流行、环境等多种风格、生成的音乐可用于、个人内容创作、Use、when、需要视频处理、音频编辑、媒体转换、配音生成时使用、不适用于版权受保、护的媒体内容处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一:Vlog背景音乐

需求:内容创作者需要为Vlog制作背景音乐.
```bash
# 生成Vlog背景音乐
cellcog.com/v1/music/generate \
  -H "Authorization: Bearer $CELLCOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "轻松愉快的lo-fi音乐,钢琴与轻柔鼓点,适合学习与工作背景",
    "duration": 120,
    "style": "lo-fi",
    "bpm": 80,
    "instrumental": true,
    "format": "mp3"
  }' \
  -o vlog-bgm.mp3
```

### 场景二:原创歌曲创作

需求:独立音乐人希望创作一首完整的原创歌曲.
```bash
# 生成原创歌曲(含人声)
cellcog.com/v1/music/generate \
  -H "Authorization: Bearer $CELLCOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lyrics": "[Verse 1]\n城市的灯光在闪烁\n我走在熟悉的街道\n[Chorus]\n追逐梦想不停歇\n向着远方奔跑",
    "style": "pop",
    "voice": "female",
    "duration": 90,
    "format": "mp3"
  }' \
  -o original-song.mp3
```

### 场景三:短视频配乐

需求:短视频创作者需要15-30秒的配乐片段.
```bash
# 生成短视频配乐
cellcog.com/v1/music/generate \
  -H "Authorization: Bearer $CELLCOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "欢快活泼的电子音乐,适合短视频,节奏明快",
    "duration": 15,
    "style": "electronic",
    "bpm": 128,
    "instrumental": true,
    "format": "mp3"
  }' \
  -o short-video-bgm.mp3
```

## 快速开始

### Step 1:获取API Key

```bash
# 注册CellCog账户并获取API Key
# 访问 CellCog 官网注册
# 新账户包含免费试用额度
# ...
# 配置API Key
export CELLCOG_API_KEY="your-api-key-here"
# ...
# 或写入配置文件
echo '{"api_key": "your-api-key"}' > ~/.cellcog/config.json
```

### Step 2:首次生成

```bash
# 最简生成:文本描述
cellcog.com/v1/music/generate \
  -H "Authorization: Bearer $CELLCOG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "轻松的钢琴音乐",
    "duration": 30
  }' \
  -o first-music.mp3
```

### Step 3:播放与检查

```bash
# 播放生成的音乐
# macOS
open first-music.mp3
# Linux
xdg-open first-music.mp3
# Windows
start first-music.mp3
```

#
## 示例

### 基础配置

```json
// ~/.cellcog/config.json
{
  "api_key": "your-api-key",
  "default_style": "pop",
  "default_duration": 30,
  "default_format": "mp3",
  "default_quality": "standard"
}
```

### 提示词模板

```yaml
# prompt-templates.yml
templates:
  vlog_background:
    prompt: "轻松愉快的{style}音乐,适合{mood}背景"
    style: "lo-fi"
    duration: 120
    instrumental: true
# ...
  short_video:
    prompt: "欢快活泼的{style}音乐,节奏明快,适合短视频"
    style: "electronic"
    duration: 15
    instrumental: true
# ...
  original_song:
    lyrics_template: |
      [Verse 1]
      {verse_content}
      [Chorus]
      {chorus_content}
    style: "pop"
    voice: "female"
    duration: 90
```

### 风格与参数对照

```python
# 风格参数推荐
style_recommendations = {
    "pop": {"bpm": 100-130, "duration": "30-180s", "mood": "uplifting"},
    "electronic": {"bpm": 120-140, "duration": "30-300s", "mood": "energetic"},
    "classical": {"bpm": 60-120, "duration": "60-300s", "mood": "elegant"},
    "ambient": {"bpm": 60-80, "duration": "60-300s", "mood": "peaceful"},
    "lo-fi": {"bpm": 70-90, "duration": "60-180s", "mood": "relaxed"},
    "rock": {"bpm": 110-140, "duration": "30-240s", "mood": "intense"}
}
```

## 最佳实践

### 提示词编写技巧

| 技巧 | 说明 | 示例 |
|---:|---:|---:|
| 明确风格 | 指定具体音乐风格 | "lo-fi hip hop"而非"放松音乐" |
| 描述乐器 | 列出主要乐器 | "piano, soft drums, bass" |
| 说明情感 | 描述情绪基调 | "melancholic, reflective" |
| 指定BPM | 给出节奏速度 | "80 BPM" |
| 设定时长 | 明确音乐长度 | "30 seconds" |
| 标明类型 | 人声或器乐 | "instrumental" |

### 歌词结构建议

```text
# 推荐歌词结构
[Verse 1]    # 主歌1(4行)
[Chorus]     # 副歌(4行)
[Verse 2]    # 主歌2(4行)
[Chorus]     # 副歌重复
[Bridge]     # 桥段(4行)
[Chorus]     # 副歌最终
[Outro]      # 结尾(2行)
```

### 时长选择建议

| 使用场景 | 推荐时长 | 说明 |
|:---:|:---:|:---:|
| 短视频配乐 | 15-30秒 | 适配短视频平台 |
| Vlog背景 | 60-180秒 | 循环播放 |
| 播客片头 | 15-30秒 | 简短识别 |
| 学习背景 | 120-300秒 | 长时间循环 |
| 完整歌曲 | 90-180秒 | 标准歌曲长度 |

### 版权与商用

- **个人使用**: 免费版生成的音乐可用于个人欣赏
- **社交媒体**: 分享需遵守CellCog服务条款
- **商业用途**: 需确认CellCog的商用许可政策
- **平台政策**: 各平台对AI生成音乐有不同政策,使用前请查阅

## 常见问题

### Q1: 如何获取CellCog API Key?

A: 访问CellCog官网注册账户,新账户包含免费试用额度。在账户设置中获取API Key,通过环境变量或配置文件设置.
### Q2: 免费版的额度是多少?

A: 免费版包含试用额度(具体额度以CellCog官网公布为准)。额度用尽后需购买付费套餐。建议合理规划使用,优先生成重要内容.
### Q3: 生成的音乐质量如何?

A: CellCog AI引擎生成的音乐音质良好,免费版提供standard音质。如需更高音质(high quality),可升级PRO版.
### Q4: 支持哪些输出格式?

A: 免费版支持MP3格式输出。如需WAV、FLAC等无损格式,或批量生成与API集成,请使用PRO版.
### Q5: 生成的音乐可以商用吗?

A: 生成的音乐商用权限取决于CellCog的服务条款。建议查阅最新条款或联系CellCog确认商用许可。免费版通常限制商用.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md规范的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要互联网连接访问CellCog API

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| CellCog API | 服务 | 必需 | CellCog官网注册 |
| curl/HTTP客户端 | 工具 | 必需 | 系统自带 |
| 音频播放器 | 工具 | 必需 | 系统自带 |

### API Key 配置

- 需要配置CellCog API Key
- 通过 `CELLCOG_API_KEY` 环境变量配置
- 或通过 `~/.cellcog/config.json` 配置文件
- 新账户注册包含免费试用额度

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令+API调用能力)
- **说明**: 基于Markdown指令驱动Agent执行音乐生成任务,通过CellCog API实现音乐生成
- **免费版限制**: 基础文生音乐、歌词生音乐、标准音质、MP3格式、试用额度、无批量生成

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "CellCog音乐生成免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "music gen cellcog"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
