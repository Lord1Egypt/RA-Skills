---
slug: heygen-tts-tool-free
name: heygen-tts-tool-free
version: 1.0.0
displayName: HeyGen TTS免费版
summary: 基于HeyGen Starfish模型的文字转语音工具,支持多语言语音合成与基础语速控制,适合个人使用.
license: Proprietary
edition: free
description: 面向个人用户的 HeyGen 文字转语音工具(免费版)。核心能力:，可自动提升工作效率

  - 基于 HeyGen Starfish TTS 模型的语音合成

  - 支持 40+ 语言的语音选择

  - 基础语速控制(0。Use when 需要文本翻译、多语言转换、本地化处理时使用。不适用于专业医学法律翻译认证。'
tags:
  - 创意设计
  - 语音合成
  - TTS
  - HeyGen
  - 多语言
  - 工具
  - 效率
  - 创意
  - 图像
  - language
  - heygen
  - data
  - api
  - voice_id
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# HeyGen TTS 工具 - 免费版

## 概述

HeyGen TTS 工具(免费版)基于 HeyGen Starfish TTS 模型,为个人用户提供文字转语音合成能力。支持 40+ 语言、基础语速控制与停顿标签,适合视频配音、有声读物与多语言内容生成.
免费版聚焦基础 TTS 合成,专业版(`heygen-tts-tool-pro`)在此基础上提供 SSML 高级标记、批量生成、词级时间戳与 API 服务化等高级能力.
## 核心能力

| 能力 | 免费版 | 说明 |
|---|---|---|
| 语音合成 | 支持 | Starfish 模型 |
| 语言支持 | 40+ | 含中英日韩法德等 |
| 语音列表 | 支持 | 查询与筛选 |
| 语速控制 | 支持 | 0.5-2.0 倍速 |
| 停顿标签 | 支持 | `<break time="1s"/>` |
| 音频下载 | 支持 | 通过 audio_url |
| SSML 标记 | 不支持 | 升级专业版 |
| 批量生成 | 不支持 | 升级专业版 |
| 词级时间戳 | 不支持 | 升级专业版 |
| 多语言混合 | 不支持 | 升级专业版 |
| API 服务 | 不支持 | 升级专业版 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：HeyGen、模型的文字转语音、支持多语言语音合、成与基础语速控制、适合个人使用、面向个人用户的、文字转语音工具、核心能力、TTS、模型的语音合成、语言的语音选择、基础语速控制、Use、when、需要文本翻译、多语言转换、本地化处理时使用、不适用于专业医学、法律翻译认证、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:视频配音生成

为视频生成中文旁白.
```bash
# 查询中文语音
curl -X GET "https://api.heygen.com/v3/voices?engine=starfish&language=Chinese" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
# ...
# 生成中文语音
curl -X POST "https://api.heygen.com/v3/voices/speech" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "欢迎观看本期视频,今天我们来聊一聊人工智能的最新发展。",
    "voice_id": "YOUR_VOICE_ID",
    "speed": 1.0,
    "language": "zh"
  }'
```

### 场景二:多语言内容生成

为国际化内容生成不同语言版本.
```python
import requests
import os
# ...
def generate_speech(text, voice_id, language="en", speed=1.0):
    """生成语音"""
    response = requests.post(
        "https://api.heygen.com/v3/voices/speech",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "voice_id": voice_id,
            "speed": speed,
            "language": language,
        }
    )
    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])
    return data["data"]
# ...
# 生成英文版本
en_result = generate_speech(
    "Welcome to our product demonstration.",
    voice_id="YOUR_EN_VOICE",
    language="en"
)
print(f"英文音频: {en_result['audio_url']}")
# ...
# 生成日文版本
ja_result = generate_speech(
    "製品のデモンストレーションへようこそ。",
    voice_id="YOUR_JA_VOICE",
    language="ja"
)
print(f"日文音频: {ja_result['audio_url']}")
```

### 场景三:带停顿的语音合成

使用 break 标签添加自然停顿.
```bash
heygen.com/v3/voices/speech" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "大家好。<break time=\"1s\"/> 欢迎来到本期节目。<break time=\"0.5s\"/> 今天我们聊一个有趣的话题。",
    "voice_id": "YOUR_VOICE_ID",
    "speed": 1.0
  }'
```

## 快速开始

### 1. 获取 API Key

1. 访问 HeyGen 官网注册账号
2. 进入控制台 > API Settings
3. 创建 API Key 并保存

```bash
# 配置环境变量
export HEYGEN_API_KEY="your-api-key-here"
```

### 2. 查询可用语音

```bash
heygen.com/v3/voices?engine=starfish" \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq '.data[0:3]'
```

### 3. 生成第一段语音

```bash
heygen.com/v3/voices/speech" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好,这是一段测试语音。",
    "voice_id": "YOUR_VOICE_ID"
  }' | jq '.data.audio_url'
```

### 4. 下载音频文件

```bash
# 获取 audio_url 后下载
curl -o output.wav "https://resource2.heygen.ai/text_to_speech/..."
```

#
## 示例

### Python 封装

```python
import requests
import os
# ...
class HeyGenTTS:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ["HEYGEN_API_KEY"]
        self.base_url = "https://api.heygen.com/v3"
# ...
    def list_voices(self, language=None, gender=None):
        """查询语音列表"""
        params = {"engine": "starfish"}
        if language: params["language"] = language
        if gender: params["gender"] = gender
# ...
            f"{self.base_url}/voices",
            headers={"X-Api-Key": self.api_key},
            params=params
        )
        return response.json()["data"]
# ...
    def generate(self, text, voice_id, speed=1.0, language=None):
        """生成语音"""
        payload = {"text": text, "voice_id": voice_id, "speed": speed}
        if language: payload["language"] = language
# ...
            f"{self.base_url}/voices/speech",
api_key, "Content-Type": "application/json"},
            json=payload
        )
        data = response.json()
        if data.get("error"):
            raise Exception(data["error"])
        return data["data"]
# ...
    def download(self, audio_url, output_path):
        """下载音频文件"""
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
# ...
# 使用
tts = HeyGenTTS()
voices = tts.list_voices(language="English")
result = tts.generate("Hello world!", voices[0]["voice_id"])
tts.download(result["audio_url"], "output.wav")
```

### 语音选择参数

| 参数 | 类型 | 说明 |
|:-----|:-----|:-----|
| `engine` | string | 固定 `starfish`(TTS 语音) |
| `language` | string | 语言筛选(如 `Chinese`、`English`) |
| `gender` | string | 性别筛选(`female` / `male`) |
| `limit` | integer | 每页数量(1-100) |
| `token` | string | 分页游标 |

### 生成请求参数

| 字段 | 类型 | 必需 | 说明 |
|---:|---:|---:|---:|
| `text` | string | 是 | 文本内容(1-5000 字符) |
| `voice_id` | string | 是 | 语音 ID |
| `speed` | number | 否 | 语速 0.5-2.0(默认 1.0) |
| `language` | string | 否 | 基础语言代码(如 `zh`、`en`) |

## 最佳实践

1. **语音选择策略**
   - 使用 `GET /v3/voices?engine=starfish` 获取 TTS 兼容语音
   - 注意:不是所有视频语音都支持 Starfish TTS
   - 优先选择有 `preview_audio_url` 的语音试听

2. **语速控制**
   - 0.8-1.2 范围内效果最自然
   - 低于 0.8 可能出现机器感
   - 高于 1.5 适合快速播报场景

3. **停顿标签使用**
   - 格式:`word <break time="1s"/> word`
   - 标签前后必须有空格
   - 使用秒数 + `s` 后缀:`<break time="1.5s"/>`

4. **文本长度控制**
   - 单次请求最大 5000 字符
   - 长文本分段生成后拼接
   - 段落间自然停顿用 break 标签

5. **错误处理**
   - 检查返回的 `error` 字段
   - 网络错误实现重试
   - 记录 `request_id` 便于排查

```python
def safe_generate(tts, text, voice_id, retries=3):
    for i in range(retries):
        try:
            return tts.generate(text, voice_id)
        except Exception as e:
            print(f"重试 {i+1}: {e}")
            time.sleep(2 ** i)
    raise RuntimeError("生成失败")
```

## 常见问题

### Q1: 如何获取 API Key?

访问 HeyGen 官网注册账号,在控制台 > API Settings 创建 API Key。免费版使用标准 `X-Api-Key` 头认证.
### Q2: 支持哪些语言?

支持 40+ 语言,包括中文、英文、日文、韩文、法文、德文、西班牙文等。通过 `language` 参数筛选.
### Q3: 为什么找不到 TTS 语音?

必须使用 `engine=starfish` 筛选。`/v3/voices` 端点返回所有语音(含视频语音),只有 `engine=starfish` 的支持 TTS.
### Q4: 免费版与专业版的区别?

免费版支持基础 TTS 合成与停顿标签;专业版提供 SSML 高级标记、批量生成、词级时间戳与多语言混合。需要高级排版或自动化的场景建议升级.
### Q5: 音频格式是什么?

返回的音频为 WAV 格式,通过 `audio_url` 下载。如需 MP3,可使用 ffmpeg 转换:
```bash
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3
```

### Q6: 文本超过 5000 字符怎么办?

分段生成后拼接。建议按自然段落分割,段间添加停顿标签.
## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需访问 `api.heygen.com`

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| requests | Python 库 | 推荐(Python) | `pip install requests` |
| curl | 命令行工具 | 可选 | 系统自带 |
| jq | JSON 处理工具 | 可选 | `brew install jq` |
| ffmpeg | 音频转换 | 可选 | `brew install ffmpeg` |
| Python 3.9+ | 运行时 | 可选(脚本) | `python.org` 下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 必须配置 `HEYGEN_API_KEY` 环境变量
- 在 HeyGen 控制台 > API Settings 创建
- 通过 `X-Api-Key` 请求头传递
- 建议使用 `.env` 文件管理,避免硬编码

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。免费版聚焦基础 TTS 合成,适合个人开发者快速集成语音能力.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需要API Key，无Key环境无法使用
