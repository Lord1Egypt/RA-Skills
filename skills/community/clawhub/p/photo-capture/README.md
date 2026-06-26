# 📷 Photo Capture Skill

[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue.svg)](https://github.com/Laurc2004/photo-capture-skills)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A cross-platform webcam capture skill for AI agents. Capture photos directly from your webcam on macOS, Windows, or Linux without requiring screen recording, accessibility, or automation permissions.

---

## [English](#english) | [中文](#中文)

---

# English

## 🎯 What is this?

**Photo Capture Skill** is an AgentSkill that enables AI assistants (like OpenClaw, Codex, etc.) to capture webcam images across different operating systems. It prioritizes direct camera access via ffmpeg, making it lightweight and permission-friendly.

## ✨ Features

- 🖥️ **Cross-platform**: Works on macOS, Windows, and Linux
- 🚀 **No complex permissions**: Uses direct camera capture (ffmpeg) instead of screen recording
- 🎛️ **Flexible configuration**: Specify device, resolution, warmup time
- 🤖 **Agent-friendly**: Designed to be used by AI agents via shell commands
- 🔄 **Automatic fallback**: macOS includes Photo Booth/FaceTime screenshot fallback

## 📦 Requirements

- **ffmpeg** must be installed and available in `PATH`

### Installing ffmpeg

| Platform | Command |
|----------|---------|
| **macOS** | `brew install ffmpeg` |
| **Windows** | `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org) |
| **Linux (Debian/Ubuntu)** | `sudo apt install ffmpeg` |
| **Linux (Fedora)** | `sudo dnf install ffmpeg` |
| **Linux (Arch)** | `sudo pacman -S ffmpeg` |

## 🚀 Quick Start

### List available cameras

```bash
python3 scripts/capture_webcam.py --list-devices
```

Example output:
```
📷 Available camera devices:
  [0] FaceTime HD Camera
  [1] OBS Virtual Camera
```

### Capture a photo

```bash
# Capture from default camera
python3 scripts/capture_webcam.py --output photo.jpg

# Capture from specific device
python3 scripts/capture_webcam.py --device 1 --output photo.jpg

# High resolution capture
python3 scripts/capture_webcam.py --width 1920 --height 1080 --output hd_photo.jpg
```

## ⚙️ Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output` | *(required)* | Output file path |
| `--device` | *(auto)* | Camera device ID, name, or path |
| `--width` | 1280 | Video width in pixels |
| `--height` | 720 | Video height in pixels |
| `--fps` | 30 | Frames per second |
| `--warmup` | 1.0 | Seconds to wait for auto-exposure |
| `--list-devices` | - | List cameras and exit |

## 🍎 macOS Fallback (Optional)

If direct ffmpeg capture doesn't work on macOS, you can use the Photo Booth fallback:

```bash
bash scripts/capture_via_app.sh \
  --app "Photo Booth" \
  --layout large \
  --capture window \
  --output photo.png
```

> ⚠️ This fallback requires Screen Recording, Accessibility, and Automation permissions.

## 🔧 How it works

```
┌─────────────────────────────────────────────────────────┐
│                    Photo Capture Flow                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   User request ──► Skill triggers ──► Run script        │
│                                              │           │
│                                              ▼           │
│                                    ┌─────────────────┐   │
│                                    │   Detect OS    │   │
│                                    └────────┬────────┘   │
│                                             │            │
│                    ┌────────────────────────┼─────────┐  │
│                    │                        │         │  │
│                    ▼                        ▼         ▼  │
│              ┌─────────┐            ┌─────────┐ ┌──────┐│
│              │ macOS   │            │ Windows │ │ Linux││
│              │avfound. │            │ dshow   │ │ v4l2 ││
│              └────┬────┘            └────┬────┘ └──┬───┘│
│                   │                      │         │    │
│                   └──────────┬───────────┘         │    │
│                              ▼                     │    │
│                    ┌─────────────────┐             │    │
│                    │  ffmpeg capture │             │    │
│                    └────────┬────────┘             │    │
│                             │                      │    │
│                             ▼                      │    │
│                    ┌─────────────────┐             │    │
│                    │   Save image    │◄────────────┘    │
│                    └─────────────────┘                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🛡️ Permissions Note

- **Direct capture (recommended)**: May trigger a one-time OS camera permission prompt for your terminal/Python
- **macOS fallback**: Requires Screen Recording + Accessibility + Automation permissions

Direct capture is preferred because it's lighter and more portable.

## 📁 Project Structure

```
photo-capture/
├── SKILL.md                      # Skill definition for AI agents
├── README.md                     # This file
└── scripts/
    ├── capture_webcam.py         # Primary cross-platform capture script
    ├── capture_via_app.sh        # macOS Photo Booth fallback (bash)
    └── capture_via_app.py        # macOS Photo Booth fallback (python)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

# 中文

## 🎯 这是什么？

**Photo Capture Skill** 是一个跨平台的摄像头拍照技能，专为 AI 助手（如 OpenClaw、Codex 等）设计。它通过 ffmpeg 直接访问摄像头，无需复杂的屏幕录制或辅助功能权限。

## ✨ 特性

- 🖥️ **跨平台**: 支持 macOS、Windows 和 Linux
- 🚀 **权限友好**: 使用 ffmpeg 直接捕获，无需屏幕录制权限
- 🎛️ **灵活配置**: 可指定设备、分辨率、预热时间
- 🤖 **AI 友好**: 专为 AI Agent 通过 shell 命令调用设计
- 🔄 **自动降级**: macOS 包含 Photo Booth/FaceTime 截图备用方案

## 📦 环境要求

- **ffmpeg** 必须已安装并在 `PATH` 中可用

### 安装 ffmpeg

| 平台 | 命令 |
|------|------|
| **macOS** | `brew install ffmpeg` |
| **Windows** | `winget install ffmpeg` 或从 [ffmpeg.org](https://ffmpeg.org) 下载 |
| **Linux (Debian/Ubuntu)** | `sudo apt install ffmpeg` |
| **Linux (Fedora)** | `sudo dnf install ffmpeg` |
| **Linux (Arch)** | `sudo pacman -S ffmpeg` |

## 🚀 快速开始

### 列出可用摄像头

```bash
python3 scripts/capture_webcam.py --list-devices
```

示例输出:
```
📷 Available camera devices:
  [0] FaceTime HD Camera
  [1] OBS Virtual Camera
```

### 拍照

```bash
# 使用默认摄像头拍照
python3 scripts/capture_webcam.py --output photo.jpg

# 指定设备拍照
python3 scripts/capture_webcam.py --device 1 --output photo.jpg

# 高分辨率拍照
python3 scripts/capture_webcam.py --width 1920 --height 1080 --output hd_photo.jpg
```

## ⚙️ 命令参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--output` | *(必填)* | 输出文件路径 |
| `--device` | *(自动)* | 摄像头设备 ID、名称或路径 |
| `--width` | 1280 | 视频宽度（像素） |
| `--height` | 720 | 视频高度（像素） |
| `--fps` | 30 | 帧率 |
| `--warmup` | 1.0 | 预热等待时间（秒），用于自动曝光调整 |
| `--list-devices` | - | 列出摄像头并退出 |

## 🍎 macOS 备用方案（可选）

如果直接 ffmpeg 捕获在 macOS 上不工作，可以使用 Photo Booth 备用方案：

```bash
bash scripts/capture_via_app.sh \
  --app "Photo Booth" \
  --layout large \
  --capture window \
  --output photo.png
```

> ⚠️ 此备用方案需要屏幕录制、辅助功能和自动化权限。

## 🔧 工作原理

```
┌─────────────────────────────────────────────────────────┐
│                    拍照流程                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   用户请求 ──► 技能触发 ──► 运行脚本                      │
│                              │                          │
│                              ▼                          │
│                    ┌─────────────────┐                  │
│                    │    检测系统     │                  │
│                    └────────┬────────┘                  │
│                             │                           │
│        ┌────────────────────┼─────────────────┐        │
│        │                    │                 │        │
│        ▼                    ▼                 ▼        │
│  ┌──────────┐        ┌──────────┐      ┌──────────┐    │
│  │  macOS   │        │ Windows  │      │  Linux   │    │
│  │avfound.  │        │  dshow   │      │  v4l2    │    │
│  └────┬─────┘        └────┬─────┘      └────┬─────┘    │
│       │                   │                 │          │
│       └─────────┬─────────┘                 │          │
│                 ▼                           │          │
│        ┌─────────────────┐                  │          │
│        │  ffmpeg 捕获    │                  │          │
│        └────────┬────────┘                  │          │
│                 │                           │          │
│                 ▼                           │          │
│        ┌─────────────────┐                  │          │
│        │   保存图片      │◄─────────────────┘          │
│        └─────────────────┘                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🛡️ 权限说明

- **直接捕获（推荐）**: 可能会触发一次性的系统摄像头权限弹窗
- **macOS 备用方案**: 需要屏幕录制 + 辅助功能 + 自动化权限

推荐使用直接捕获，更轻量且更便携。

## 📁 项目结构

```
photo-capture/
├── SKILL.md                      # AI Agent 技能定义
├── README.md                     # 本文件
└── scripts/
    ├── capture_webcam.py         # 主要跨平台拍照脚本
    ├── capture_via_app.sh        # macOS Photo Booth 备用 (bash)
    └── capture_via_app.py        # macOS Photo Booth 备用 (python)
```

## 🤝 参与贡献

欢迎提交 Issue 或 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

Made with ❤️ for AI agents everywhere 🤖