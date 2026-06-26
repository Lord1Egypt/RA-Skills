# Movie Subtitle Viewer for OpenClaw

让 AI 通过字幕「看」电影的 OpenClaw 技能。

## 功能

- 🎬 通过 OpenSubtitles API 搜索电影字幕
- 📄 解析 .srt/.ass 字幕文件
- 📖 提取电影台词，让 AI 理解剧情

## 安装

```bash
pip install pysubs2 requests
```

## 使用方法

### 1. 设置环境变量

```bash
# 创建 .env 文件（不要提交到 Git！）
OPENSUBTITLES_API_KEY=your_api_key
OPENSUBTITLES_USERNAME=your_username
OPENSUBTITLES_PASSWORD=your_password
```

### 2. 搜索并下载字幕

```python
from src.subtitle_client import SubtitleClient

client = SubtitleClient()
client.login()

# 搜索字幕
results = client.search("Artificial Intelligence", year=2001, language="en")
print(f"Found {len(results)} subtitles")

# 下载字幕
subtitle = client.download(results[0], save_path="movie.srt")

# 解析字幕
from src.subtitle_parser import parse_subtitle
lines = parse_subtitle("movie.srt")
for line in lines[:10]:
    print(line)
```

### 3. 获取剧情摘要

```python
from src.movie_summary import generate_summary

summary = generate_summary("movie.srt")
print(summary)
```

## 示例：让小溪「看」《人工智能》

```python
# 1. 登录
client = SubtitleClient()
client.login()

# 2. 搜索并下载
results = client.search("Artificial Intelligence", year=2001, language="en")
subtitle_path = client.download(results[0])

# 3. 解析
lines = parse_subtitle(subtitle_path)

# 4. 让 AI 理解
# 将 lines 发送给 AI，让它总结剧情
```

## 目录结构

```
movie-subtitle-viewer/
├── src/
│   ├── __init__.py
│   ├── subtitle_client.py   # OpenSubtitles API 客户端
│   ├── subtitle_parser.py    # 字幕解析器
│   └── movie_summary.py     # 剧情摘要生成
├── .env.example             # 环境变量示例
├── README.md
└── requirements.txt
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENSUBTITLES_API_KEY` | OpenSubtitles API Key |
| `OPENSUBTITLES_USERNAME` | OpenSubtitles 用户名 |
| `OPENSUBTITLES_PASSWORD` | OpenSubtitles 密码 |

## 注意事项

⚠️ **不要提交敏感信息！**
- `.env` 文件已加入 `.gitignore`
- 使用前复制 `.env.example` 为 `.env` 并填入你的凭据

## 参考

- [OpenSubtitles API](https://opensubtitles.stoplight.io)
- [pysubs2](https://github.com/Arcanemagus/pysubs2)

---

🦞 Made with love for OpenClaw!
