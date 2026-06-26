# Provider 对接说明（当前版）

## 总原则
- 文本人格回复：由 ChatGPT / Claw 当前会话模型直接完成。
- ASR / TTS：由 SenseAudio 完成。
- 不再要求配置 `AUDIOZEN_API_KEY`。

## 推荐环境变量
```env
SENSEAUDIO_API_KEY=你的token
SENSEAUDIO_BASE_URL=https://api.senseaudio.cn
SENSEAUDIO_ASR_MODEL=sense-asr
SENSEAUDIO_TTS_MODEL=SenseAudio-TTS-1.0
FFMPEG_PATH=/opt/homebrew/bin/ffmpeg  # 可选，Mac 常用
```

## 可选本地文件
脚本会按以下顺序尝试补充配置：
1. 当前进程环境变量
2. Skill 根目录下的 `.env.local`
3. Skill 根目录下的 `.env`

环境变量优先级最高。

## ASR 接口
- 路径：`/v1/audio/transcriptions`
- 鉴权：`Authorization: Bearer <SENSEAUDIO_API_KEY>`
- 默认模型：`sense-asr`

## TTS 接口
- 路径：`/v1/t2a_v2`
- 鉴权：`Authorization: Bearer <SENSEAUDIO_API_KEY>`
- 默认模型：`SenseAudio-TTS-1.0`
- 当前只建议使用免费可用音色：
  - `child_0001_a`
  - `child_0001_b`
  - `male_0004_a`
  - `male_0018_a`

## 回复模式建议
- `text`：只返回文本，适合飞书 / Lark 日常聊天。
- `audio`：只生成音频，适合“发语音版”场景。
- `both`：同时返回文本和音频路径，适合服务端二次分发。
- `auto`：默认模式；在 `channel=feishu` 时等价于文本优先。


## ffmpeg
- 默认直接执行系统 PATH 里的 `ffmpeg`。
- 如果 PicoClaw / 飞书机器人运行环境拿不到 PATH，显式设置：`FFMPEG_PATH=/opt/homebrew/bin/ffmpeg`。
- 该变量只影响 MP3 转 OPUS 的步骤。
