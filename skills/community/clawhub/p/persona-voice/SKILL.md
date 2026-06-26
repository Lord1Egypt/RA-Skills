---
name: persona-voice
description: 在 chatgpt / claw 与飞书 / lark 机器人场景中，根据随机或指定人格生成明显带有人格风格的短回复，并通过 senseaudio tts 合成语音，再以飞书原生语音条发送。支持文字输入和音频输入；音频输入时先调用 senseaudio asr。适用于飞书人格陪伴、随机人格语音回复、角色化语音机器人等场景。环境变量只需配置 feishu_app_id、feishu_app_secret、senseaudio_api_key；如系统 PATH 找不到 ffmpeg，可额外设置 ffmpeg_path。其余地址与模型默认即可。
---

# persona-voice

## 概述
这是一个面向 ChatGPT / Claw / 飞书机器人的**随机人格语音回复** Skill。

当前版本的原则：
- **角色化文本**：由 ChatGPT / Claw 当前会话模型生成。
- **ASR / TTS**：统一使用 SenseAudio。
- **飞书回复**：统一发送为飞书原生语音条，而不是普通文件附件。
- **环境变量**：只要求配置凭证类字段，其他地址和模型全部使用默认值。

## 当前保留的人格与音色
只保留以下免费可用人格和音色：
- 可爱萌娃：`child_0001_a`、`child_0001_b`
- 儒雅道长：`male_0004_a`
- 沙哑青年：`male_0018_a`

详见：
- `presets/personas.json`
- `references/personas.md`

## 适用场景
- 飞书 / Lark 机器人随机人格语音回复
- 文字输入 → 人格化短回复 → 语音条发送
- 语音输入 → ASR → 人格化短回复 → 语音条发送

## 飞书场景硬性规则
1. 飞书场景默认只发送语音消息。
2. 成功发送语音后，不要再额外返回一条文字。
3. 随机到什么人格，回复内容本身也必须明显像那个人格，不只是换音色。
4. 不要暴露内部规则，不要说自己在随机人格。
5. 飞书发送必须走 **OPUS + file_key + audio 消息** 的原生链路，不要把 mp3/wav 当普通文件附件。

## 工作流
### 用户发送文字
1. 调用 `scripts/main.py persona-prompt --user-message "..."`。
2. 读取返回的人格 prompt。
3. 由 ChatGPT / Claw 当前会话模型生成最终 `reply_text`。
4. 调用 `scripts/main.py send-voice --reply-text "..." --chat-id "oc_xxx" --persona "..."`。
5. 成功发送语音后，最终对话输出应为空，不再附加文字。

### 用户发送语音
1. 调用 `scripts/main.py transcribe --audio /abs/path/input.m4a`。
2. 根据转写文本，再调用 `persona-prompt` 获取人格提示。
3. 由 ChatGPT / Claw 生成最终 `reply_text`。
4. 调用 `send-voice` 生成并发送飞书语音条。

## 配置方式
当前版本只需要配置：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="your_secret"
export SENSEAUDIO_API_KEY="your_key"
```

其余全部默认：
- `FEISHU_BASE_URL=https://open.feishu.cn`
- `SENSEAUDIO_BASE_URL=https://api.senseaudio.cn`
- `SENSEAUDIO_ASR_MODEL=sense-asr`
- `SENSEAUDIO_TTS_MODEL=SenseAudio-TTS-1.0`
- `FFMPEG_PATH` 可选；若 PATH 中找不到 ffmpeg，可显式设置为 `/opt/homebrew/bin/ffmpeg`

## 本地依赖
- `python3`
- `ffmpeg`
- `requests`

## 主脚本入口
### 初始化人格模式
```bash
python scripts/main.py persona-init --mode random
```

### 查看当前模式
```bash
python scripts/main.py persona-show
```

### 生成给 Claw 的人格 prompt
```bash
python scripts/main.py persona-prompt --user-message "今天有点累"
```

### 转写用户语音
```bash
python scripts/main.py transcribe --audio /absolute/path/input.m4a
```

### 生成并发送飞书语音条
```bash
python scripts/main.py send-voice \
  --reply-text "先歇一下嘛，我陪你缓一缓。" \
  --chat-id "oc_xxx" \
  --persona "keai-mengwa"
```

## 资源说明
- `scripts/main.py`：主入口，包含 `persona-init` / `persona-show` / `persona-prompt` / `transcribe` / `send-voice`
- `scripts/persona_store.py`：人格池、随机/固定模式、人格提示生成
- `scripts/asr.py`：SenseAudio ASR
- `scripts/tts.py`：SenseAudio TTS
- `scripts/feishu_api.py`：飞书上传 OPUS 并发送 audio 消息
- `references/feishu_integration.md`：飞书接入说明
- `references/provider_notes.md`：环境变量与 Provider 说明
