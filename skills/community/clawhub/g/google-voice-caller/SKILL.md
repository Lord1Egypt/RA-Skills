---
name: google-voice-caller
version: 1.1.1
description: Automate Google Voice calls with AI-generated voice (TTS) or local audio injection.
invocations:
  - words:
      - 打电话给
      - 给.*打电话
      - 拨通
      - call
      - dial
    description: Automatically extract phone numbers and messages from natural language to execute a call.
---

# google-voice-caller 📞

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

一个让你的 OpenClaw Agent 具备物理外呼能力的黑科技插件。它通过无头浏览器（Puppeteer）直接驱动 Google Voice 网页端，实现低成本、自动化的语音通话。

### ✨ 核心特性
- **自动拨号**：支持全球号码拨打（遵循 Google Voice 费率）。
- **音频注入**：支持将 AI 生成的语音（TTS）或本地 `.wav` 文件直接“灌入”通话，对方接听即可听到。
- **自然语言交互**：直接对 Agent 说“给主人打个电话说开会了”，即可自动触发。
- **持久会话**：通过 Cookie 注入，无需反复登录验证。

### 🛠️ 前置要求
1. **Google Voice 账户**：且账户内有足够余额（拨打非美加号码）。
2. **环境依赖**：`chromium`, `ffmpeg`, `puppeteer-core`。
3. **认证信息**：在技能目录下准备好 `google_voice_cookies.json`。

### 🚀 快速开始
> "打电话给 +8615912345678 告诉他文档已经写好了。"

---

## English

A powerful plugin that grants your OpenClaw Agent the ability to make physical phone calls. It drives the Google Voice web interface via a headless browser (Puppeteer), enabling low-cost, automated voice communication.

### ✨ Key Features
- **Automated Dialing**: Supports global calling (following Google Voice rates).
- **Audio Injection**: Directly inject AI-generated voice (TTS) or local `.wav` files into the call stream.
- **Natural Language Interaction**: Just say "Call my boss and tell him I'm on my way" to trigger the action.
- **Persistent Session**: Uses cookie injection to skip repetitive login verifications.

### 🛠️ Prerequisites
1. **Google Voice Account**: Ensure sufficient balance for non-US/Canada calls.
2. **Environment**: `chromium`, `ffmpeg`, `puppeteer-core`.
3. **Auth**: Place `google_voice_cookies.json` in the skill directory.

### 🚀 Quick Start
> "Call +1234567890 and say the report is ready."

---

## ⚙️ Parameters / 参数说明

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--number` | ✅ | - | Target number (E.164 format) |
| `--text` | ❌ | - | Text to speak (Auto TTS) |
| `--audio` | ❌ | - | Local audio path (.wav) |
| `--duration` | ❌ | 60 | Call duration in seconds |

## ⚠️ Security & Privacy
- Keep your `google_voice_cookies.json` secure.
- Comply with local laws. Do NOT use for harassment or illegal activities.

---
**Author**: Joe & OpenClaw Assistant
**License**: MIT
