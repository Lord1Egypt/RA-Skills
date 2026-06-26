---
name: feishu-voice
description: 通过 Edge TTS 把文字转语音，发送到飞书。支持纯语音发送和文字+语音同时发送。环境变量配置，无硬编码凭证，完全免费无需 API Key。触发词：飞书语音、发语音、feishu voice、语音发送、文字转语音
---

# Feishu Voice — 飞书语音发送工具

用 Edge TTS 把文字转语音，直接发到飞书。无需 API Key，完全免费。凭证通过环境变量传递，不硬编码。

## 依赖

- `edge-tts` — Microsoft Edge TTS
- `ffmpeg` — 音频格式转换（mp3 → opus）
- `curl` / `python3`

安装：
```bash
pip install edge-tts
# ffmpeg: apt install ffmpeg 或 brew install ffmpeg
```

## 配置（环境变量）

```bash
export FEISHU_APP_ID="cli_xxxxxx"
export FEISHU_APP_SECRET="xxxxxxxx"
export FEISHU_RECEIVE_ID="ou_xxxxx"   # 或用群聊
```

## 使用方法

### 1. feishu-voice-send.sh（纯语音）

```bash
./feishu-voice-send.sh "你好，这是语音消息"
./feishu-voice-send.sh "你好" "ou_xxxxx" "zh-CN-YunxiNeural"
```

**可用中文语音：**
| 语音 | 说明 |
|------|------|
| zh-CN-XiaoxiaoNeural | 女声（晓晓） |
| zh-CN-YunxiNeural | 男声（云希） |
| zh-CN-XiaoyiNeural | 女声（晓伊） |
| zh-CN-YunyangNeural | 男声（云扬） |

### 2. feishu-send.sh（文字+语音同时发送）

```bash
./feishu-send.sh "详细文字内容..." "语音摘要，三句以内"
```

## 技术原理

```
文字 → Edge TTS → MP3 → FFmpeg(opus) → 飞书文件上传 → audio消息
```

1. Edge TTS 把文字转成 MP3（免费、无需 API Key）
2. FFmpeg 把 MP3 转成飞书要求的 OPUS 格式
3. 上传到飞书获取 file_key
4. 发送 audio 消息

## 安全说明

- 凭证通过环境变量传递，**不硬编码**
- 适合 CI/CD 和生产环境

## 交流群

👉 [点击加入飞书交流群](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=d32n52ca-753a-4b2e-a1c4-d5c977d64ca3)

永久邀请链接，加入后即可参与讨论、提问和获取更新通知。

## 项目地址

https://github.com/Mayiv-Ai/feishu-voice
