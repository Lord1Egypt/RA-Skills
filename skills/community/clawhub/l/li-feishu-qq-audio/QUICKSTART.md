# Li Feishu Audio - 快速开始

## 1. 安装

```bash
cd /root/.openclaw/skills/li-feishu-audio
./scripts/install.sh
```

## 2. 测试

```bash
# 完整功能测试
.venv/bin/python test_voice.py
```

## 3. 重启 OpenClaw

```bash
openclaw gateway restart
```

## 4. 使用

在飞书发送语音消息，AI 会自动：
1. 识别你的语音 → 文字
2. 生成 AI 回复 → 文字
3. 合成回复语音 → opus 文件
4. 发送语音回复 → 飞书

## 手动调试

```bash
# 语音识别
./scripts/fast-whisper-fast.sh audio.wav

# 语音生成
./scripts/tts-voice.sh "你好" output.mp3

# 飞书发送
./scripts/feishu-tts.sh output.mp3 user_open_id
```

## 配置

确保 `~/.openclaw/openclaw.json` 中有飞书配置：

```json
{
  "extensions": {
    "openclaw-lark": {
      "appId": "your-app-id",
      "appSecret": "your-app-secret"
    }
  }
}
```
