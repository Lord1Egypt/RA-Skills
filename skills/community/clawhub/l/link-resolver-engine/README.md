# 🚀 OpenClaw Skill: 抖音 & B站全能高清视频下载器 (Video Downloader)

这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) 定制的专属综合下载 Skill。本插件旨在解析**抖音（Douyin）**与**哔哩哔哩（Bilibili）**的视频链接，精准提取最高画质的直链，并提供稳定可靠的本地下载与音视频合并功能。

针对不同平台的反爬策略，本 Skill 综合使用了 `Playwright` 动态拦截、`Requests` 原生请求、正则表达式提取以及 `yt-dlp` 封装库，极大提高了视频解析与下载的成功率。

## ✨ 核心特性

- **🔗 智能链接解析**：自动识别并展开 `v.douyin.com` 与 `b23.tv` 各种短链接。
- **🎬 B站全功能下载**：支持 `Requests` 纯请求抓取（自动调用 FFmpeg 合并音视频）以及 `yt-dlp` 双重下载引擎。
- **📱 抖音最高画质提取**：通过无头浏览器拦截动态请求获取最高比特率（Bit Rate）无水印直链，并配备移动端页面备用解析方案。
- **🚫 突破水印限制**：智能转换播放链接，获取纯净无水印视频。
- **🕵️‍♂️ 反爬虫绕过**：内置 `tf-playwright-stealth` 和伪造请求头，有效隐藏浏览器与爬虫特征。
- **📂 自动文件管理**：支持自定义下载目录，自动按平台、时间戳和视频 ID 生成规范的文件名。

## 🛠️ 环境依赖

本 Skill 运行时依赖以下 Python 库（代码内部已通过 `ensure_package` 模块自动检查并安装）：

- `requests`
- `playwright`
- `tf-playwright-stealth`
- `yt-dlp`

### ⚠️ 系统依赖 (重要)
由于 B站的高清视频通常是**视频轨与音频轨分离**的，本 Skill 在合并 B站音视频时依赖系统级别的 **FFmpeg**：
- 请确保你的操作系统已安装 [FFmpeg](https://ffmpeg.org/download.html)，并且将其添加到了系统的环境变量（PATH）中，否则 `download_bilibili_video_request` 方法将会失败并只保留无声视频。
- **浏览器内核**：首次运行代码时，系统会自动执行 `playwright install chromium` 以下载必要的浏览器内核。

## 💻 核心方法 (API)

本 Skill 提供了针对双平台的独立解析和下载函数：

### 🎵 抖音 (Douyin) 模块

- **`expand_douyin_url(short_url: str) -> tuple[bool, str]`**
  展开 `v.douyin.com` 短链。返回 `(是否成功, 完整 URL 或 错误信息)`。
- **`get_douyin_no_wm(raw_url: str) -> str | None`**
  通过 Playwright 拦截网页请求，获取最高画质的无水印直链。
- **`download_douyin_video(no_wm_url: str, filename: str = None, download_dir: str = None) -> bool`**
  带 Referer 请求头下载抖音无水印视频。
- **`download_douyin_video_mobile(short_url: str, ... ) -> tuple[bool, str]`**
  备选方案。模拟移动端访问，直接从 HTML/JSON 中正则提取视频流并下载。

### 📺 哔哩哔哩 (Bilibili) 模块

- **`expand_bilibili_url(short_url: str) -> tuple[bool, str]`**
  展开 `b23.tv` 格式的短链接。返回 `(是否成功, 完整 URL 或 错误信息)`。
- **`get_bilibili_no_wm(raw_url: str) -> dict | None`**
  纯 requests 提取器，避开 Playwright 解码问题。通过模拟 WBI 参数获取 B站视频流和音频流的直链，返回包含 `video_url` 和 `audio_url` 的字典。
- **`download_bilibili_video_request(play_info: dict, filename: str = None, download_dir: str = None) -> bool`**
  下载 B站视频流与音频流，并自动调用 FFmpeg 进行无损合并。
- **`download_bilibili_video_yt_dlp(url: str, ... ) -> tuple[bool, str]`**
  极其稳定的封装方案。直接调用 `yt-dlp` 进行 B站视频下载，自动选择最佳音视频轨并合并，支持指定下载目录。

## 📖 参数说明

| 参数 (短) | 参数 (长)           | 描述 |
|----------|--------------------|------|
| `-u`     | `--url`            | **(必需)** 视频链接，支持长链、短链、带参数链接 |
| `-p`     | `--filename-prefix`| *(可选)* 自定义文件名前缀，默认使用视频标题 |
| `-d`     | `--download-dir`   | *(可选)* 下载存放路径，默认当前目录下 `downloads` |
| `-f`     | `--format`         | *(可选)* B站专用，指定 `yt-dlp` 的下载格式字符串 |

### 💻 命令行直接调用 (Terminal Usage)

你可以直接通过命令行脚本 video_snapper.py 快速下载视频。以下是针对不同场景的使用示例：

# 1. 基础下载 (默认下载到 ./downloads 目录)
python scripts/video_snapper.py -u "https://b23.tv/ReXDyVO"

# 2. 指定下载目录
python scripts/video_snapper.py -u "https://b23.tv/ReXDyVO" -d "F:/命理学"

# 3. 指定文件名前缀 + 下载目录
python scripts/video_snapper.py -u "https://b23.tv/ReXDyVO" -p "测试" -d "F:/命理学"


# 1. 基础下载 (自动去水印并提取最高画质)
python scripts/video_snapper.py -u "https://v.douyin.com/ezOqxZPY3kc/"

# 2. 指定下载目录
python scripts/video_snapper.py -u "https://v.douyin.com/ezOqxZPY3kc/" -d "F:/命理学"

# 3. 指定文件名前缀 + 下载目录
python scripts/video_snapper.py -u "https://v.douyin.com/ezOqxZPY3kc/" -p "测试" -d "F:/命理学"

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

下载这个视频 https://www.bilibili.com/video/BV1MU95BsEey/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=b845b6e7ad62d0465263434acf42945b

这个B站视频下下来 https://www.bilibili.com/video/BV1ExX6BGELJ/?spm_id_from=333.1007.tianma.3-1-7.click&vd_source=b845b6e7ad62d0465263434acf42945b

视频下载器，帮我处理这个：https://www.douyin.com/jingxuan?modal_id=7624114795335257353

这个视频保存到F盘命名张雪机车https://www.douyin.com/jingxuan?modal_id=7611124804929785115
