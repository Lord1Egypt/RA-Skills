# 渠道格式说明

## 为什么需要格式转换？

不同平台对语音消息的要求不同：

- **飞书/Telegram/WhatsApp** - 要求 opus 编码的 ogg 格式才能显示为语音消息
- **Discord/Signal/Slack** - 只能显示为文件附件

## 格式对照表

| 渠道 | 推荐格式 | 编码 | 消息类型 | 说明 |
|------|----------|------|----------|------|
| feishu | ogg | libopus | 语音消息 | ✅ 真正的语音 |
| telegram | ogg | libopus | 语音消息 | ✅ 真正的语音 |
| whatsapp | ogg | libopus | 语音消息 | ✅ 真正的语音 |
| discord | mp3 | libmp3lame | 文件 | 文件附件 |
| signal | mp3 | libmp3lame | 文件 | 文件附件 |
| slack | mp3 | libmp3lame | 文件 | 文件附件 |

## FFmpeg 转换命令

### WAV → OGG (opus)
```bash
ffmpeg -y -i input.wav -c:a libopus -b:a 64k output.ogg
```

### WAV → MP3
```bash
ffmpeg -y -i input.wav -c:a libmp3lame -q:a 2 output.mp3
```

## OpenClaw 飞书插件逻辑

```javascript
// media.ts 第 274-277 行
const msgType = fileType === "opus" ? "audio" : fileType === "mp4" ? "media" : "file";
```

- `opus` → 发送 `msg_type: "audio"` → 语音消息
- 其他 → 发送 `msg_type: "file"` → 文件附件

## 最佳实践

### 飞书语音消息
```bash
# 必须用 ogg 格式
python3 scripts/tts.py --text "测试" --channel feishu --reference_audio voice.ogg
```

### Discord 文件
```bash
# mp3 即可
python3 scripts/tts.py --text "测试" --channel discord --reference_audio voice.ogg
```

## 注意事项

1. **文件后缀** - 必须是 `.ogg`，不能是 `.oga`
2. **编码** - 必须是 `libopus`，不是默认编码
3. **比特率** - 推荐 64k，足够清晰
