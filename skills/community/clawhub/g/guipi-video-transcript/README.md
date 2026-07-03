# 视频文案提取 · WorkBuddy Skill

从本地视频文件中提取语音文案/字幕，完全离线运行。跨平台支持 macOS / Windows / Linux。

## 特性

- 🎬 **一键提取**：MP4 → 文案，一条命令搞定
- 🖥️ **跨平台**：macOS（Metal GPU 加速）/ Windows / Linux 全支持
- 🔒 **完全离线**：无需网络，数据不上传
- 🤖 **智能引擎**：自动检测环境选择最优转录引擎
  - macOS：whisper-cpp（Metal GPU 加速，brew 安装）
  - Windows：openai-whisper（pip 自动安装）
  - Linux：whisper-cpp 优先，自动 fallback

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「视频文案提取」一键安装。

### 手动安装

```bash
# 克隆仓库到 WorkBuddy 技能目录
git clone https://github.com/guipi888/workbuddy-video-transcript.git \
  ~/.workbuddy/skills/video-transcript
```

### 环境依赖

**macOS**：
```bash
brew install ffmpeg whisper-cpp
```

**Windows**：
```bash
# 安装 ffmpeg
winget install ffmpeg
# 或从 https://ffmpeg.org/download.html 下载
```

**Linux**：
```bash
sudo apt install ffmpeg
```

## 使用

```bash
python3 scripts/pipeline.py "视频.mp4" "./output/" [模型大小] [语言]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| 视频路径 | ✅ | 本地视频文件绝对路径 |
| 输出目录 | ✅ | 输出 WAV 和 TXT 的目录 |
| 模型大小 | ❌ | `tiny` / `base` / `small`，默认 `base` |
| 语言 | ❌ | 默认 `zh` |

### 示例

```bash
# 基本用法
python3 scripts/pipeline.py ~/Downloads/video.mp4 ./output/

# 使用 tiny 模型（更快）
python3 scripts/pipeline.py ~/Downloads/video.mp4 ./output/ tiny

# 转录英文视频
python3 scripts/pipeline.py ~/Downloads/video.mp4 ./output/ base en
```

## 输出

- `{视频名}.wav` — 提取的 16kHz 单声道音频
- `{视频名}.txt` — 转录文案

## 项目结构

```
├── SKILL.md              # WorkBuddy 技能定义
├── README.md             # 本文件
├── LICENSE               # MIT
├── .gitignore
├── assets/
│   └── author-qrcode.jpg # 作者二维码
└── scripts/
    ├── extract_audio.py  # ffmpeg 音频提取
    ├── transcribe.py     # 转录引擎（跨平台）
    └── pipeline.py       # 一键管道
```

## 作者

**桂皮AI实战** — 专注 AI 工具教程 · 扣子编程 · 效率方法

- 公众号 / 小红书 / 抖音：桂皮AI实战
- 知识星球：桂皮AI实战

## License

MIT License — 详见 [LICENSE](./LICENSE)
