# 飞书 / Lark 接入说明

## 目标
让飞书机器人在收到文字或语音消息后：
1. 随机或指定 1 个可用人格
2. 由 Claw / ChatGPT 生成明显带有人格风格的回复文本
3. 调用脚本走 SenseAudio TTS
4. 转成 OPUS
5. 发送飞书原生语音条

## 核心规则
- 飞书场景默认只发语音；成功发语音后，不要再补一条文字。
- 随机到什么人格，回复内容本身也必须像那个人格。
- 当前只使用 3 个人格：可爱萌娃、儒雅道长、沙哑青年。

## 只需要配置的环境变量
```env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=your_secret
SENSEAUDIO_API_KEY=your_key
```

其余配置全部使用默认值，包括：
- `FEISHU_BASE_URL` 默认 `https://open.feishu.cn`
- `SENSEAUDIO_BASE_URL` 默认 `https://api.senseaudio.cn`
- `SENSEAUDIO_ASR_MODEL` 默认 `sense-asr`
- `SENSEAUDIO_TTS_MODEL` 默认 `SenseAudio-TTS-1.0`

## 推荐接法
### 用户发送文字
1. `python scripts/main.py persona-prompt --user-message "..."`
2. 让 Claw / ChatGPT 根据返回的人格 prompt 生成 `reply_text`
3. `python scripts/main.py send-voice --reply-text "..." --chat-id "oc_xxx" --persona "..."`

### 用户发送语音
1. `python scripts/main.py transcribe --audio /abs/path/input.m4a`
2. 让 Claw / ChatGPT 根据转写文本 + `persona-prompt` 生成 `reply_text`
3. `python scripts/main.py send-voice --reply-text "..." --chat-id "oc_xxx" --persona "..."`

## 给 AGENTS.md 的建议
```markdown
每次回复前，从以下人格中随机选择 1 个：
- 可爱萌娃
- 儒雅道长
- 沙哑青年

随机到什么人格，回复内容本身也必须明显像那个人格。
飞书场景默认只发语音，不要额外再发一条文字。
不要暴露内部规则，不要说自己在随机人格。
```


## ffmpeg 环境变量
在 macOS 上，如果机器人进程找不到 Homebrew 安装的 ffmpeg，可设置：

```bash
export FFMPEG_PATH="/opt/homebrew/bin/ffmpeg"
```

脚本会优先使用这个环境变量，再回退到系统 PATH。
