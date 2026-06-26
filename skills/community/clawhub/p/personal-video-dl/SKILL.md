---
name: personal-video-dl
description: 视频下载工具，支持YouTube、Bilibili、抖音等数千个网站。触发词："下载视频"、"视频下载"
version: 1.0.0
---

# 视频下载工具

基于 yt-dlp 的强大视频下载工具，支持数千个视频网站。

## 功能特性

- ✅ **多平台支持**：YouTube、Bilibili、抖音、TikTok、西瓜视频、微博等
- ✅ **智能识别**：自动识别视频平台
- ✅ **格式选择**：支持最佳质量、仅音频、指定格式
- ✅ **批量下载**：支持从文件批量下载
- ✅ **字幕下载**：可选下载视频字幕
- ✅ **播放列表**：支持下载整个播放列表

## 触发方式

```
下载视频 https://www.youtube.com/watch?v=xxxxx
视频下载 "B站链接" --audio-only
帮我下载这个视频：抖音链接
```

## 使用方法

### 命令行使用

```bash
# 下载单个视频（最佳质量）
python3 video_downloader.py "https://www.youtube.com/watch?v=xxxxx"

# 仅下载音频（MP3）
python3 video_downloader.py "URL" --audio-only

# 指定下载目录
python3 video_downloader.py "URL" -o ~/Desktop/Videos

# 下载带字幕
python3 video_downloader.py "URL" --subtitle

# 批量下载（从文件）
python3 video_downloader.py -f urls.txt
```

### 批量下载文件格式

创建 `urls.txt` 文件：
```
# 这是注释
https://www.youtube.com/watch?v=xxxxx
https://www.bilibili.com/video/xxxxx
https://v.douyin.com/xxxxx
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `url` | 视频链接 | `"https://..."` |
| `-f, --file` | 批量下载文件 | `-f urls.txt` |
| `-o, --output` | 下载目录 | `-o ~/Videos` |
| `-q, --quality` | 视频质量 | `-q best` |
| `-a, --audio-only` | 仅音频 | `--audio-only` |
| `-s, --subtitle` | 下载字幕 | `--subtitle` |
| `-p, --playlist` | 下载播放列表 | `--playlist` |

## 支持的平台

- **国际**: YouTube、TikTok、Instagram、Twitter/X、Facebook、Reddit
- **国内**: Bilibili、抖音、西瓜视频、微博
- **其他**: 数千个网站（详见 yt-dlp 支持列表）

## 前置依赖

```bash
# 安装 yt-dlp
pip install -U yt-dlp

# 或使用脚本安装
python3 video_downloader.py --install
```

## 输出

- **默认目录**: `~/Downloads/Videos/`
- **文件命名**: `视频标题.扩展名`
- **音频格式**: MP3
- **视频格式**: MP4

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| yt-dlp 未安装 | 运行 `pip install -U yt-dlp` |
| 下载失败 | 检查网络连接，部分网站需要代理 |
| 格式不支持 | 尝试更新 yt-dlp: `pip install -U yt-dlp` |
| 权限错误 | 检查下载目录写入权限 |

## 技术说明

- **底层工具**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Python 版本**: 3.7+
- **依赖**: yt-dlp

## 文件结构

```
skills/video-downloader/
├── SKILL.md              # 本说明文件
└── video_downloader.py   # 主脚本
```

---
*Created: 2026-03-08*
