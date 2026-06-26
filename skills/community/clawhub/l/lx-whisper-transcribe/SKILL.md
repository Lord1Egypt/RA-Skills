---
name: lx-whisper-transcribe
description: OpenClaw语音转文字技能 - 使用whisper.cpp实现本地语音识别，完全本地处理，无需API密钥，支持中文。
version: 1.1.0
author: 小曦
interpreter: bash
tags:
  - whisper
  - speech-to-text
  - voice
  - local
  - chinese
triggers:
  - 语音转文字
  - 转录音频
  - 语音识别
  - 听写
scripts:
  - path: whisper
    interpreter: bash
    description: 语音转文字包装器脚本
permissions:
  - exec:ffmpeg
  - exec:wget
  - exec:curl
  - filesystem:read
  - filesystem:write_cache
---

# lx-whisper-transcribe

OpenClaw语音转文字技能 - 使用whisper.cpp实现本地语音识别

## 描述

此技能解决OpenClaw升级后语音消息无法被转录为文字的问题。通过使用whisper.cpp和国内镜像源，提供完全本地化的中文语音转文字功能，无需API密钥。

## 功能

- ✅ 接收并转录语音消息为文字
- ✅ 支持中文语音识别
- ✅ 使用本地模型，无需API密钥
- ✅ 在网络受限环境下通过国内镜像源正常工作

## 触发条件

当用户提到“语音转文字”、“转录音频”、“语音识别”或类似关键词时，应激活此技能。

## 使用方法

```bash
whisper /path/to/audio.ogg
注意事项
- 首次使用需要下载模型文件
- 需要预先编译 whisper.cpp
- 需要安装 ffmpeg
```