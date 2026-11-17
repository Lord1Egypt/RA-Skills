# 音视频内容加工台

[English](README.md)

本地查看媒体信息、提取音轨、剪辑、抽帧，生成 SRT/VTT 字幕；可选本地转录，分段缓存便于继续处理。

## 功能

本地查看媒体信息、提取音轨、剪辑、抽帧，生成 SRT/VTT 字幕；可选本地转录，分段缓存便于继续处理。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
检查我上传的视频，列出时长、分辨率、音视频编码和文件大小。
```

```text
把这段视频的第12至35秒剪成新文件，在片段中抽两张预览图。
```

```text
从这个视频提取音轨，把我提供的时间戳文字生成SRT和VTT字幕。
```

文件在本机处理，输出片段、预览、字幕和处理清单。转录为可选模块，首次使用需下载本地模型；不需要 MochiLab 服务端或转录 API Key。

## 运行要求

Python 3.10+, FFmpeg (or imageio-ffmpeg 0.6+), PyAV 14–16, Pillow 12+; optional faster-whisper 1.2+ for local transcription

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-media-workbench
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-media-workbench)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-media-workbench
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-media-workbench)。下载仓库 ZIP，将 `skills/mochi-media-workbench` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
