# 视频文案提取 · WorkBuddy Skill

"从本地视频文件中提取语音文案/字幕。跨平台支持macOS/Windows/Linux，完全离线运行。使用whisper模型进行高精度语音识别，支持多语言字幕提取和OCR文字识别。触发词：视频文案提取、提取字幕、语音转文字、视频转文字、提取文案。"

## 特性

- 用户提供本地 MP4 视频文件路径，要求"提取文案"、"语音转文字"、"提取字幕"
- 需要将视频口播内容整理为文字稿
- 从抖音/B站/小红书等下载的视频中提取口播文案
- **需要带时间戳的字幕文件导入剪辑软件**（剪映/PR/达芬奇/FCPX）
- **中英混合视频的自动识别转录**（auto 模式自动检测语言切换）

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「视频文案提取」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/video-transcript.git \
  ~/.workbuddy/skills/video-transcript
```

### 环境依赖

请参考 SKILL.md 中的环境要求章节

## 使用

```bash
python3 ~/.workbuddy/skills/video-transcript/scripts/pipeline.py \
  "<视频文件路径>" \
  "<输出目录>" \
  [模型大小] [语言]
```

## 输出

- `{视频名}.wav` — 提取的 16kHz 单声道音频
- `{视频名}.txt` — 转录文案（纯文本，无时间戳）
- `{视频名}.srt` — 字幕文件（带时间戳，可直接导入剪辑软件）

## 项目结构

```
.gitignore
LICENSE
SKILL.md
```

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」|
| 💬 公众号 | 微信搜「桂皮AI实战」|
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意）|

## License

MIT License — 详见 [LICENSE](./LICENSE)
