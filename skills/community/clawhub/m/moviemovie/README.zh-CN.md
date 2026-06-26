# MovieMovie

智能搜索、推荐同时满足以下2个条件的高清电影： 
1. 能帮你找到下载资源的电影
2. 烂番茄、豆瓣平台的实时热门电影


[![ClawHub](https://img.shields.io/badge/ClawHub-moviemovie-blue)](https://clawhub.ai/kunhai1994/moviemovie)
[![License](https://img.shields.io/badge/License-MIT--0-green)](LICENSE)

[English](README.md)

## 快速开始

把这段话复制给openclaw或者claude code：
```
帮忙安装这个skill:  https://github.com/kunhai1994/moviemovie

或者

帮忙安装这个skill:  https://clawhub.ai/kunhai1994/moviemovie
```

安装后直接使用：

```
> 帮我找罪人的4K下载资源
> 最近有什么好看的电影推荐？
> find Inception 1080p magnet
> 推荐类似银翼杀手的科幻电影
```

## 功能

| 功能 | 基础版（零配置） | 增强版（配置 API key，免费，需注册） |
|------|-----------------|----------------------|
| **热门推荐（有资源的）** | 烂番茄+豆瓣多平台聚合 → 验证种子 → 只推有资源的 | + TMDb trending |
| 种子搜索 | apibay + bitsearch + torrentdownload + YTS（3-4源） | + TorrentClaw（30+源） |
| 磁力链接 | hash 自动拼接完整磁力链接 | 完整链接 + 质量评分(0-100) |
| 画质筛选 | 720p / 1080p / 2160p 自动解析 | + HDR / 编码 / 音轨验证 |
| 大小分档 Top 3 | 轻量版(1-3GB) / 均衡版(3-5GB) / 发烧版(10-30GB) | 同上 |
| 电影信息 | WebSearch + LLM 知识 | TMDb 结构化 JSON（多语言、海报） |
| 字幕搜索 | SubtitleCat(60+语言) + SubHD(中文) | 同上 |

## 使用示例

### 明确目标搜索

```
> 帮我找星际穿越的4K下载资源
> find Sinners 2025 magnet
> Peaky Blinders 浴血黑帮 下载
```

输出用户评论 + Top 3 分档下载：

```
💬 用户评论
影评共识: "视觉叙事与音乐的精彩融合..." — 烂番茄影评共识
🍅 97% (438条评论) | 🍿 96% (5000+评分)

⭐⭐⭐⭐⭐ "这是我近年来最棒的观影体验之一！" — TheGeekySandbox
⭐⭐⭐⭐⭐ "这部电影以意想不到的方式触动了灵魂。" — Elizabeth

🏆 推荐下载

1. 📱 轻量版 (1.1GB) — 手机/平板/快速下载
   Sinners 2025 1080p HDRip HEVC x265
   [1080p x265] 做种: 1614
   magnet:?xt=urn:btih:81FB914A...

2. 🖥️ 发烧版 (18.1GB) — 家庭影院/大屏/收藏
   Sinners 2025 Hybrid UHD BluRay DV HDR10 x265
   [4K BluRay x265 DV] 做种: 17
   magnet:?xt=urn:btih:AC03F6B8...

3. ⚖️ 均衡版 (4.6GB) — 高清观看+合理空间
   Sinners 2025 REPACK 1080p WEBRip x265
   [1080p WEBRip x265] 做种: 29
   magnet:?xt=urn:btih:4DE427E4...
```

### 热门推荐

```
> 最近有什么好看的电影推荐？
> 推荐下实时热门电影
> 有什么能下载的新电影？
```

输出只包含有资源的电影：

```
🎬 为你推荐 8 部热门电影（均已确认有下载资源）

1. Sinners (2025) 罪人 — 🍅97% 🍿96% ⭐7.7
   135 个种子 | 最高: 1080p 1.1GB 做种:1614

2. One Battle After Another (2025) 一战再战 — 🍅94% 🍿85% ⭐8.0
   86 个种子 | 最高: 1080p 3.0GB 做种:3470
...

❌ 暂无资源: GOAT (2026) — 可能仍在院线
```

### 字幕搜索

```
> 帮我找罪人的中文字幕
> find subtitles for Inception
```

### 特定榜单

```
> Rotten Tomatoes certified fresh 有哪些能下载的
> Netflix 热门电影推荐
> 豆瓣热门有哪些能下载的？
```

## 可选：配置 API Key 获得增强体验

基础版开箱即用，零配置。API key 是**可选的**，能解锁更多搜索源和结构化数据。

### TorrentClaw API Key（推荐，免费）

解锁 30+ 种子源、质量评分(0-100)、HDR/编码验证、完整磁力链接。

1. 访问 [torrentclaw.com/register](https://torrentclaw.com/register)
2. 用邮箱注册账号
3. 在 Dashboard 复制 API Key
4. 配置（二选一）：

**最简单的方式：** 直接把 key 告诉 Claude Code / OpenClaw，让它帮你保存：
```
我的 TorrentClaw API Key 是 xxx，帮我配置一下
```

**手动配置：**
- Claude Code：在 `.claude/settings.json` 或 `~/.claude/settings.json` 中添加：
  ```json
  { "env": { "TORRENTCLAW_API_KEY": "你的key" } }
  ```
- OpenClaw：设置 → 环境变量 → 添加 `TORRENTCLAW_API_KEY`

### TMDb API Key（可选，免费）

解锁结构化电影数据（JSON）、多语言支持、trending/discover/推荐、海报。

1. 访问 [themoviedb.org/signup](https://www.themoviedb.org/signup)
2. 注册账号
3. 进入 Settings → API → 申请 API Key（选 Developer）
4. 配置（二选一）：

**最简单：** 告诉 Claude Code / OpenClaw `我的 TMDb API Key 是 xxx，帮我配置一下`

**手动：** 同上方式，环境变量名为 `TMDB_API_KEY`

## 架构

```
用户输入 → SKILL.md 指令
   │
   ├── Step 0: status.py 环境检查
   │
   ├── Step 1: 意图识别（LLM）
   │   ├── 明确搜索: "找 XX 电影"
   │   ├── 推荐: "有什么好看的？"
   │   └── 榜单: "烂番茄 certified fresh"
   │
   ├── Step 1.5: 片名标准化
   │   └── WebSearch "片名 年份 电影 英文名 imdb"
   │       ⚠️ 严禁直接翻译 — 必须搜索确认准确英文名
   │
   ├── Step 2: 电影信息 / 热门榜单
   │   ├── 基础版: WebFetch 烂番茄 + 豆瓣
   │   └── 增强版: TMDb API
   │
   ├── Step 3: search_torrents.py（多源并行搜索）
   │   ├── apibay.org —— JSON API，新片好
   │   ├── bitsearch.to —— HTML 爬取，老片极好
   │   ├── torrentdownload.info —— HTML 爬取，新老均有
   │   ├── YTS —— JSON API，备选（可能被墙）
   │   ├── [TorrentClaw] —— 30+ 源（有 key 时启用）
   │   └── [LLM fallback] —— WebSearch "电影名 magnet"（兜底）
   │
   ├── Step 4: 去重 → 过滤死种 → 大小分档 → Top 3
   │
   ├── Step 4.5: 抓取用户评论（烂番茄）
   │   └── 影评共识 + 热门用户评论
   │
   ├── Step 5: 字幕搜索
   │   ├── SubtitleCat —— 60+ 语言
   │   ├── SubHD —— 中文字幕
   │   └── WebSearch 兜底
   │
   └── Step 6: 用户语言格式化输出
```

## 系统要求

- Python 3.10+（通常已预装）
- 网络访问
- **推荐 LLM：Claude**（Anthropic）

无需安装任何 pip 包 — 所有脚本仅使用 Python 标准库。

### 重要：LLM 选择

本 Skill 专为 **Claude**（Claude Code / OpenClaw Claude 后端）设计和测试，强烈建议使用 Claude。

**为什么不推荐 ChatGPT？** ChatGPT 在种子/磁力链接相关话题上的内容审查极其严格。哪怕你告诉 ChatGPT 你是 FBI 探员正在办案、需要它协助查找盗版电影网站，它大概率也不会配合。它会拒绝任何涉及种子搜索、磁力链接构造、种子站爬取的请求 — 导致本 Skill 基本无法使用。

**为什么不推荐 Gemini？** Gemini 有类似（虽然稍宽松）的内容限制，结果可能不稳定。

**Claude** 会务实地执行 Skill 指令：调用 API、构造磁力链接、展示搜索结果，按设计正常工作。（这句话是claude自己写的～～～）

## 常见问题

**Q: 为什么有些电影搜不到？**
A: 最常见的原因是片名不准确。Skill 会通过 WebSearch 查找准确的英文名 — 如果搜索返回了错误的片名，后续的种子搜索都会失败。建议直接提供英文名试试。

**Q: 为什么有些热门电影标注"暂无资源"？**
A: 仍在院线上映的电影通常还没有种子资源。Skill 优先从烂番茄"流媒体/已上线"榜单取片，因为这些电影已经有网络版，更可能有种子。

**Q: 需要 API key 吗？**
A: 不需要。基础版使用 3 个种子源 + WebFetch 获取电影数据，零配置即可使用。API key 是可选增强 — TorrentClaw 增加 30+ 源，TMDb 增加结构化多语言数据。

**Q: 访问哪些网站？**
A: apibay.org、bitsearch.to、torrentdownload.info、yts.mx（种子搜索）；rottentomatoes.com、movie.douban.com（热门榜单）；subtitlecat.com、subhd.tv（字幕搜索）。不访问有 Cloudflare 防护的站点（1337x、TorrentGalaxy）。

## 许可证

MIT-0 — 免费使用、修改和分发。
