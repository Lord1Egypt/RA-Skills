---
name: gv-caller
version: 1.0.1
description: 使用 Google Voice 自动拨打电话并播放 AI 生成的语音（TTS）或本地音频。
invocations:
  - words:
      - 打电话给
      - 给.*打电话
      - 拨通
      - call
    description: 自动从自然语言中提取号码和消息并执行拨号。
---

# gv-caller 📞

一个让你的 OpenClaw Agent 具备物理外呼能力的黑科技插件。它通过无头浏览器（Puppeteer）直接驱动 Google Voice 网页端，实现低成本、自动化的语音通话。

## ✨ 核心特性
- **自动拨号**：支持全球号码拨打（遵循 Google Voice 费率）。
- **音频注入**：支持将 AI 生成的语音（TTS）或本地 `.wav` 文件直接“灌入”通话，对方接听即可听到。
- **自然语言交互**：直接对 Agent 说“给主人打个电话说开会了”，即可自动触发。
- **持久会话**：通过 Cookie 注入，无需反复登录验证。

## 🛠️ 前置要求
1. **Google Voice 账户**：且账户内有足够余额（拨打非美加号码）。
2. **环境依赖**：
   - `chromium` 浏览器
   - `ffmpeg` (用于音频转码)
   - `puppeteer-core` (Node.js 库)
3. **认证信息**：需在技能目录下准备好 `google_voice_cookies.json`。

## 🚀 快速开始

### 1. 自动提取信息拨打
直接在飞书/控制台对 Agent 说：
> "打电话给 +8615912345678 告诉他文档已经写好了。"

### 2. 命令行手动调用
```bash
# 拨打并朗读指定文字
openclaw skills run gv-caller -- --number +86159xxxx --text "你好，任务已完成"

# 拨打并播放本地音频文件
openclaw skills run gv-caller -- --number +86159xxxx --audio /tmp/music.wav --duration 30
```

## ⚙️ 配置说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--number` | ✅ | - | 目标号码 (E.164格式) |
| `--text` | ❌ | - | 要朗读的文本，支持自动 TTS 转语音 |
| `--audio` | ❌ | - | 本地音频路径 (建议 16k/44.1k wav) |
| `--duration` | ❌ | 60 | 通话保持时长 (秒) |

## ⚠️ 安全与隐私
- 请妥善保管 `google_voice_cookies.json`，其中包含您的 Google 账户访问权限。
- 请遵守当地法律法规，严禁将本工具用于骚扰、电信诈骗或任何非法用途。

---
**Author**: Joe & OpenClaw Assistant
**License**: MIT
