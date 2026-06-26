---
name: douyin-download
description: "Download Douyin (Chinese TikTok) videos to local MP4 files. Use when the user shares a Douyin video URL or asks to download or save a Douyin/TikTok video. Works with exported browser cookies and a local HTTP proxy. Triggers: download Douyin video, save TikTok, 抖音视频下载."
version: "1.0.0"
author: musofan
homepage: "https://github.com/musofan/douyin-download"
repository: "https://github.com/musofan/douyin-download"
keywords: ["douyin", "tiktok", "video", "download", "playwright", "cookies"]

---

# Douyin Download | 抖音视频下载

> Save any Douyin video to MP4 — no watermarks, no limits.

## 特性 | Features

- 🎬 **高清下载** — 1080p MP4，无水印 / No watermark, full 1080p
- 🤖 **全自动** — 只需发链接给我，剩下的我来 / Just send the link, I'll handle the rest
- 🔒 **隐私安全** — Cookie 来自你自己的浏览器，不经过第三方 / Your cookies stay local, no third-party involved
- ⚡ **即下即用** — 拦截真实视频直链，直接下载 / Intercepts real video stream, downloads directly

## 使用前提 | Prerequisites

| 项目 | 说明 |
|------|------|
| Chrome 扩展 | 安装 [Get cookies.txt](https://chrome.google.com/webstore) (可选，如果无法下载再装) |
| 导出 Cookie | 访问 douyin.com → 点扩展 → Export → 保存到 `sessions/cookies/cookies.txt` |
| 代理 | Clash Verge 或任意 HTTP 代理，运行在 `127.0.0.1:7897` |
| Python 包 | `playwright`, `requests` |

> 注意：Cookie 只需要导出一次，除非过期。文件保存在你自己的电脑上，不会上传。

## 使用方法 | Usage

发给我任意抖音链接即可：

```
https://www.douyin.com/video/7627894054088461611
```

我会自动下载并保存到 `sessions/video-download/` 目录。

或者用命令行指定路径：

```bash
python skills/douyin-download/scripts/download.py <video_url> [output_path] [cookie_file]
```

## 工作原理 | How It Works

```
1. Playwright 启动无头浏览器 → 加载你的 cookies
2. 访问抖音页面 → Douyin 以为是真实浏览器
3. 拦截 douyinvod.com 视频响应 → 拿到真实 MP4 直链
4. 直接下载 MP4 文件 → 不经过任何第三方服务器
```

**为什么不用 yt-dlp？** 因为抖音有额外的浏览器指纹验证，导出的 cookie 缺少签名信息，yt-dlp 会报 "Fresh cookies needed"。Playwright 用真实浏览器环境解决这个限制。

## 输出 | Output

下载完成后，你会看到：
- 文件路径：`sessions/video-download/video.mp4`
- 文件大小、时长、分辨率
- 下载进度条

## 注意 | Notes

- 视频直链有过期签名，请尽快下载 / Video URLs expire quickly, download promptly
- 如果下载失败，尝试重新导出一次新鲜 cookies / If it fails, re-export fresh cookies from douyin.com
- 支持抖音和 TikTok 链接 / Supports both Douyin and TikTok URLs
