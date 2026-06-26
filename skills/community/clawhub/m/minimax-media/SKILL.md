---
name: minimax-media
description: MiniMax media skill for voice, image, video, and music generation. Use when the user asks for MiniMax, TTS, text-to-speech, voice, image generation, image-to-image, video generation, image-to-video, music generation, a single unified entrypoint, or says "用技能生成".
---

# MiniMax Media

统一入口：`scripts/minimax`

## 能力

- `tts`：语音合成
- `image`：文生图 / 图生图
- `video`：文生视频 / 图生视频
- `music`：文生音乐

## 环境变量

```env
MINIMAX_API_KEY=...
MINIMAX_API_HOST=https://api.minimaxi.com
MINIMAX_TTS_MODEL=speech-2.8-hd
MINIMAX_TTS_VOICE_ID=English_expressive_narrator
MINIMAX_IMAGE_MODEL=image-01
MINIMAX_VIDEO_MODEL=MiniMax-Hailuo-2.3
MINIMAX_MUSIC_MODEL=music-2.5+
```

## 快速用法

```bash
scripts/minimax tts "突突你好啊，我是柱子。" --output /tmp/voice.mp3
scripts/minimax image "黑白花狸花猫在电脑前敲代码" --output /tmp/cat.jpg
scripts/minimax image "把这张图改成夜景霓虹风" --input-image ./ref.jpg --output /tmp/i2i.jpg
scripts/minimax video "黑白花狸花猫在夜晚的办公室里写代码" --output /tmp/video.mp4
scripts/minimax video "把静态图做成轻微推进镜头" --input-image ./ref.jpg --output /tmp/i2v.mp4
scripts/minimax music "lofi chill, warm piano, night city vibe" "歌词"
```

## 规则

- 默认优先使用 `MINIMAX_API_HOST=https://api.minimaxi.com`
- 图 / 视频支持参考图输入；不记字段名，直接走 `scripts/minimax`
- 任务结果文件会写到当前工作目录或 `--output` 指定路径
- 需要排查时，可加 `--print-json`
- 遇到额度不足、鉴权失败、超时、返回结构异常，会直接中文报错，不会让人干等

## 你该怎么用

当用户要：
- 生成语音
- 生成图片
- 做图生图
- 生成视频
- 做图生视频
- 生成音乐

直接调用 `scripts/minimax`，不要让人类记那些 API 细节。
