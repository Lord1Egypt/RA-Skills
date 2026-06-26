---
name: music-manager
version: 1.0.0
description: 通用音乐下载管理器。支持从YouTube/Bilibili搜索下载音乐，自动转MP3，按分类存入本地音乐库
---

# Music Manager

通用音乐下载管理工具，支持从 YouTube/Bilibili 下载音频并自动归类。

## 功能

- 从 YouTube/Bilibili 搜索并下载音乐
- 自动转换为 MP3 格式
- 按分类存入本地音乐库

## 首次配置

### 1. 安装依赖

```bash
# 安装 yt-dlp（音视频下载工具）
brew install yt-dlp

# 安装 ffmpeg（音视频转换工具）
brew install ffmpeg
```

### 2. 配置音乐目录

编辑 `scripts/download_music.py`，修改配置：

```python
# 你的音乐目录路径
MUSIC_DIR = "~/Music"  # 或 "/你的/音乐/目录"
```

### 3. Cookie 配置（可选）

YouTube 下载需要登录权限：

```bash
# 方法1：从浏览器自动提取
BROWSER = "chrome"  # 或 safari, firefox

# 方法2：不使用 cookie（可能受限）
BROWSER = None
```

## 使用方法

### 命令行

```bash
python3 scripts/download_music.py "<搜索词或URL>" "<分类文件夹>"
```

**示例：**
```bash
# 搜索并下载歌曲
python3 scripts/download_music.py "周杰伦 稻香" "中文"

# 从 B 站下载视频音频
python3 scripts/download_music.py "https://www.bilibili.com/video/BVxxx" "游戏"
```

### AI Agent 调用

让 AI 帮你下载：

1. 告诉 AI 想下载什么歌
2. AI 会先搜索展示结果让你确认
3. 选择分类后自动下载

## 命名格式

下载文件自动命名为：`歌名-作者-来源.mp3`

例如：`稻香-周杰伦-youtube.mp3`
