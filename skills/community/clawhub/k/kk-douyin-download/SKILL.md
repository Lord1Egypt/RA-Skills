---
name: douyin-download
description: 抖音视频解析下载工具。从分享链接提取无水印下载地址，支持下载+转文字+内容分析。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "dirs": ["/Users/kk/.openclaw/mcp-servers/douyin-analyzer"],
            "bins": ["ffmpeg", "whisper"],
          },
        "install":
          [
            {
              "id": "git-clone",
              "kind": "manual",
              "label": "douyin-analyzer MCP 已安装在 ~/.openclaw/mcp-servers/douyin-analyzer",
            },
          ],
      },
  }
---

# 抖音视频解析下载

## 核心功能

从抖音分享链接提取无水印视频下载地址，支持：
1. **解析下载地址**（MCP 调用）
2. **下载视频**（curl）
3. **提取音频 + 转文字**（ffmpeg + whisper）
4. **内容分析**

## 使用方式

### 方式一：MCP 调用（推荐）

**已注册到 mcporter，直接可用：**
```bash
mcporter call douyin-analyzer.parse_douyin_video_info share_link="https://v.douyin.com/xxx"
mcporter call douyin-analyzer.get_douyin_download_link share_link="https://v.douyin.com/xxx"
mcporter call douyin-analyzer.analyze_douyin_video share_link="https://v.douyin.com/xxx"
```

### 方式二：直接调用 Python

```python
import sys
sys.path.insert(0, '/Users/kk/.openclaw/mcp-servers/douyin-analyzer')
from server import DouyinParser, AudioProcessor

# 1. 提取视频信息
video_id = DouyinParser.extract_video_id("https://v.douyin.com/xxx")
info = DouyinParser.get_video_info(video_id)
print(info)

# 2. 获取无水印下载链接
url = DouyinParser.get_download_url(video_id, "https://v.douyin.com/xxx")
print(f"下载链接: {url}")

# 3. 下载视频
ap = AudioProcessor()
ap.download_video(url, "/tmp/video.mp4")

# 4. 转文字（GPU加速）
ap.transcribe("/tmp/video.mp4")
```

## 解析原理

| 层 | 方法 | 说明 |
|----|------|------|
| 第一层 | `iesdouyin.com` 官方 API | 直接请求，返回 playwm 地址，替换 `playwm`→`play` |
| 第二层 | 第三方解析 API | `liuxingw.com/api/douyin/api.php` |
| 第三层 | Playwright 浏览器 | 模拟手机访问分享链接，提取 `<video>` 标签 |

**无水印原理：** `playwm` = 带水印，`play` = 无水印。替换域名即可。

## 注意事项

- **无需登录**，分享链接即可解析
- **无需 Cookie**，任何抖音视频都能解析
- Whisper 转文字推荐加 `--device mps` 用 GPU 加速
- 视频文件会暂存 `/tmp/`，用完可手动删除
