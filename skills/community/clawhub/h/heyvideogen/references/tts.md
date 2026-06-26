# TTS & Audio — Heyvideogen

## 推荐方式：复用 Videogen Harness

```bash
python skills/videogen/scripts/v2/tts_harness.py "配音文本" \
  --output heyvideogen-project/heyvideogen-output
```

## HyperFrames CLI TTS（轻量）

```bash
npx hyperframes tts "这是配音文本" \
  --voice af_nova \
  --output heyvideogen-project/narration.wav

# 查看可用音色
npx hyperframes tts --list
```

## 字幕转录

```bash
npx hyperframes transcribe heyvideogen-project/heyvideogen-output/voiceover.mp3
```

## 音频嵌入 HTML

```html
<audio
  id="vo"
  data-start="0"
  data-duration="57"
  data-track-index="2"
  data-volume="1"
  src="heyvideogen-output/voiceover.mp3">
</audio>

<audio
  id="bgm"
  data-start="0"
  data-duration="57"
  data-track-index="3"
  data-volume="0.25"
  src="bgm.mp3">
</audio>
```

## 音量控制

| 场景 | VO 音量 | BGM 音量 |
|------|--------|---------|
| 纯干货讲解 | 1.0 | 0.15-0.2 |
| 剧情+旁白 | 0.9 | 0.2-0.3 |
| 音乐驱动 | 0.8 | 0.3-0.5 |
