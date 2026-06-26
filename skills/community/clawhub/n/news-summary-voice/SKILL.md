---
version: 1.0.0
name: news-summary-voice
description: 新闻汇总与语音播报工具。获取国际可信 RSS 源新闻，生成语音摘要。当用户要求新闻更新、每日简报、世界动态、AI 播报新闻时触发。支持多语言，跨平台（macOS/Linux/Windows）。
metadata: {"openclaw": {"emoji": "📰"}}
---

# News Summary Voice 📰

新闻汇总 + 语音播报，跨平台支持。

## 触发条件

- 用户说"新闻"、"今天发生了什么"、"世界动态"
- 要求"新闻简报"、"每日总结"
- 要求"语音播报新闻"
- 定时新闻推送场景

## 支持的 RSS 源

### 国际新闻（英文）
| 来源 | RSS URL | 语言 |
|------|---------|------|
| BBC World | https://feeds.bbci.co.uk/news/world/rss.xml | EN |
| Reuters World | https://www.reutersagency.com/feed/?best-topics=world-news | EN |
| NPR News | https://feeds.npr.org/1001/rss.xml | EN |
| Al Jazeera | https://www.aljazeera.com/xml/rss/all.xml | EN |
| The Guardian | https://www.theguardian.com/world/rss | EN |
| AP News | https://rsshub.app/apnews/topics/apf-topnews | EN |

### 国内新闻（中文）
| 来源 | RSS URL | 语言 |
|------|---------|------|
| 新华网 | https://www.rss臆.com/xml/Rss臆news.xml | ZH |
| 人民网 | http://www.people.com.cn/rss/news.xml | ZH |
| 联合早报 | https://www.zaobao.com.sg/rss/realtime/china | ZH |

### 科技新闻
| 来源 | RSS URL |
|------|---------|
| Hacker News | https://news.ycombinator.com/rss |
| TechCrunch | https://techcrunch.com/feed/ |
| Ars Technica | https://feeds.arstechnica.com/arstechnica/index |

## 跨平台用法

### macOS
```bash
# 获取新闻（curl）
curl -s --max-time 10 "https://feeds.bbci.co.uk/news/world/rss.xml" | \
  grep -E '<title>|<link>' | sed 's/<[^>]*>//g' | head -20

# 语音播报（say 命令，macOS 内置）
say "Here is your news briefing."

# 播放新闻音频（curl 下载 + afplay 播放）
curl -s "音频URL" -o /tmp/news.mp3 && afplay /tmp/news.mp3
```

### Linux
```bash
# 获取新闻（curl/wget）
curl -s --max-time 10 "https://feeds.bbci.co.uk/news/world/rss.xml" | \
  grep -E '<title>|<link>' | sed 's/<[^>]*>//g' | head -20

# 语音播报（需要安装）
# Ubuntu/Debian: sudo apt install espeak-ng ffmpeg
# CentOS/RHEL: sudo yum install espeak-ng ffmpeg

# TTS 播报（espeak-ng）
espeak-ng "Here is your news briefing." 2>/dev/null

# 或用 Coze TTS 工具生成音频
```

### Windows (PowerShell)
```powershell
# 获取新闻
[xml]$rss = Invoke-WebRequest -Uri "https://feeds.bbci.co.uk/news/world/rss.xml" -UseBasicParsing
$rss.rss.channel.item | Select-Object -First 10 | ForEach-Object { $_.title }

# 语音播报（Windows TTS）
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Speak("Here is your news briefing.")
```

## 使用决策树

```
1. 用户要求新闻？
   → 确定语言（中文/英文/双语）

2. 需要哪些来源？
   → 国际热点 → BBC + Reuters + Al Jazeera
   → 国内动态 → 新华网 + 人民网 + 联合早报
   → 科技前沿 → Hacker News + TechCrunch
   → 综合 → 多源混合

3. 需要语音播报？
   → 是 → 用 Coze TTS 工具生成音频
   → 否 → 纯文本摘要

4. 时间范围？
   → 今日 → as_qdr=d 筛选
   → 本周 → as_qdr=w 筛选
   → 全部 → 无筛选
```

## 输出格式

```markdown
## 📰 新闻简报 — 2026年3月19日

### 🌍 国际头条
1. **[标题](链接)** — 摘要...
2. ...

### 🇨🇳 国内动态
1. **[标题](链接)** — 摘要...
2. ...

### 💻 科技前沿
1. **[标题](链接)** — 摘要...
2. ...

### 🎙️ 语音播报
[通过 Coze TTS 工具生成音频]

---
来源：BBC | Reuters | Al Jazeera | 新华网 | Hacker News
```

## 注意事项

- RSS 源可能失效，定期检查
- 国际新闻源国内可能访问受限
- 语音播报优先使用 Coze TTS 工具
- 敏感新闻需人工审核后播报
- 定时推送建议早起时段（7:00-8:00）执行
