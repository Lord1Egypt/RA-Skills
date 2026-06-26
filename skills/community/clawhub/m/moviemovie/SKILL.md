---
name: moviemovie
version: 1.0.0
description: |
  搜索电影下载资源（磁力链接/种子），推荐有下载资源的热门电影。
  多平台热门聚合（烂番茄+豆瓣）+ 种子资源实时验证 = 只推荐你能下载到的电影。
  触发词："找电影"、"电影下载"、"磁力"、"推荐电影"、"最近有什么好看的"、
  "find movie"、"download"、"magnet"、"trending"
argument-hint: "[电影名 或 推荐请求]"
allowed-tools: Bash Read WebSearch WebFetch Skill
author: Kunhai
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - python3
      optionalEnv:
        - TORRENTCLAW_API_KEY
        - TMDB_API_KEY
    primaryEnv: ""
    tags:
      - movie
      - torrent
      - magnet
      - download
      - recommend
      - film
      - subtitle
  gemini:
    extension_type: skill
---

# MovieMovie — 电影搜索与推荐 Skill

搜索电影种子/磁力资源，推荐有下载资源的热门电影。

**核心原则：只推荐确认有下载资源的电影。**

## Step 0: 环境检查

运行状态检查脚本，确定当前模式：

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/status.py" --json
```

解析 JSON 输出，关键字段：

- mode: "basic" 或 "enhanced" 或 "full"
- torrentclaw_key: 是否配置了 TorrentClaw API key
- tmdb_key: 是否配置了 TMDb API key
- sources: 哪些种子源可达

## Step 1: 解析用户意图

判断用户请求类型：

**A. 明确搜索** — 用户有具体电影："find Inception 4K"、"找星际穿越的磁力链接"

**B. 推荐请求** — 用户要推荐："最近有什么好看的"、"recommend trending movies"

**C. 特定榜单** — 用户要列表："豆瓣热门"、"Rotten Tomatoes certified fresh"、"Netflix 热门"

提取：片名、年份（如有）、画质偏好（4K/1080p）、用户语言。

## Step 1.5: 片名标准化

**这是整个 Skill 最关键的步骤，做错了后面全白搭。**

严禁直接翻译非英文片名！必须通过 WebSearch 查询准确英文名。

**错误示范：**

- "罪人" 翻译为 "The Sinner" — 错！这是一部美剧，不是 2025 年的电影
- "一战再战" 翻译为 "One More Fight" — 完全不对

**正确做法：**

1. 用 WebSearch 搜索: "[片名] [年份] 电影 英文名 imdb"
2. 从搜索结果中提取准确的英文名 + IMDB ID

**正确结果：**

- "罪人 2025 电影 英文名 imdb" 得到 Sinners (tt36742579)
- "一战再战 2025 电影 英文名 imdb" 得到 One Battle After Another (tt30144839)
- "夜王 2026 电影 英文名 imdb" 得到 Night King (tt37284356)

如果用户输入已经是英文，跳过此步。

## Step 2A: 搜索模式 — 获取电影信息

增强版（有 TMDB_API_KEY 时）：

```bash
curl -s "https://api.themoviedb.org/3/search/movie?api_key=$TMDB_API_KEY&query=英文片名&year=年份&language=zh-CN"
```

基础版：直接用 Step 1.5 的 WebSearch 结果，里面已包含电影信息。

## Step 2B: 推荐模式 — 多平台聚合热门榜单

并行从多个平台抓取热门列表：

**来源 1（首选）：烂番茄流媒体热门 — 已上线的电影 = 大概率有种子**

使用 WebFetch 抓取 `https://www.rottentomatoes.com/browse/movies_at_home/sort:popular`，提取所有电影的片名、烂番茄评分、观众评分、年份。

**来源 2：烂番茄院线热映 — 参考热度，但可能无资源**

使用 WebFetch 抓取 `https://www.rottentomatoes.com/browse/movies_in_theaters/sort:top_box_office`，提取相同信息。

**来源 3（中文用户）：豆瓣热门**

使用 WebFetch 抓取 `https://movie.douban.com/chart`，提取有评分的新片列表。

**增强版额外（有 TMDB_API_KEY 时）：**

```bash
curl -s "https://api.themoviedb.org/3/trending/movie/week?api_key=$TMDB_API_KEY&language=en-US"
```

**合并处理：**

1. 以英文片名为主键合并去重
2. 出现在多个榜单的电影加权优先
3. 综合评分 = (烂番茄影评分 + 观众分 + 豆瓣分x10 + 多榜加权) / 系数
4. 按综合评分排序
5. 翻译片名为用户语言
6. 取 Top 15-20 部候选，进入 Step 3 批量搜索种子
7. **只推荐有资源的电影**

### 烂番茄 URL 参考

| 用途 | URL 路径 |
|------|---------|
| 流媒体热门 | /browse/movies_at_home/sort:popular |
| 流媒体最新 | /browse/movies_at_home/sort:newest |
| 流媒体 Certified Fresh | /browse/movies_at_home/critics:certified_fresh~sort:popular |
| Netflix 热门 | /browse/movies_at_home/affiliates:netflix~sort:popular |
| 院线热映（票房） | /browse/movies_in_theaters/sort:top_box_office |
| 院线热映（评分） | /browse/movies_in_theaters/sort:tomatometer |
| 即将上映 | /browse/movies_coming_soon |

基础 URL: https://www.rottentomatoes.com

## Step 3: 搜索下载资源

### Layer 1: Python 搜索引擎（主力）

用 Step 1.5 获取的**准确英文片名**运行搜索脚本：

```bash
python3 "$CLAUDE_SKILL_DIR/scripts/search_torrents.py" "英文片名" --year 年份 --json
```

如果有 IMDB ID，加 --imdb tt1234567 提高精准度。

脚本会并行搜索 3-4 个源（apibay、bitsearch、torrentdownload、YTS），返回 JSON，包含去重排序后的结果、磁力链接和 Top 3 大小分档。

### Layer 2: LLM 兜底（脚本返回 0 结果时）

使用 WebSearch 搜索 "英文片名 年份 magnet 1080p" 和 "英文片名 年份 torrent download"。

尝试从搜索结果中提取磁力链接（以 magnet:?xt=urn:btih: 开头）。

### Layer 3: 最后兜底

如果 Layer 1 + 2 都无结果，给用户提供手动搜索链接：

- bitsearch.to/search?q=编码后的片名&category=1
- apibay.org/q.php?q=编码后的片名&cat=207

## Step 4: 结果筛选与分档

解析 search_torrents.py 的 JSON 输出，展示 Top 3 大小分档：

**推荐下载 Top 3 格式：**

1. 轻量版 (1-3GB) — 手机/平板/快速下载。通常为 1080p WEB x265 压缩版本。
2. 发烧版 (10-30GB) — 家庭影院/大屏/收藏。通常为 4K BluRay Remux DV+HDR10。
3. 均衡版 (3-5GB) — 高清观看+合理空间。通常为 1080p BluRay h264。

每档展示：画质标签、文件大小、做种数、磁力链接。

不足 3 档时有多少展示多少。优先展示 4K 资源。

**推荐模式**下只展示有资源的电影，格式示例：

> 为你推荐 8 部热门电影（均已确认有下载资源）
>
> 1. Sinners (2025) 罪人 — 烂番茄 97% 观众 96% 豆瓣 7.7 — 135 个种子，最高: 1080p 1.1GB 做种:1614
> 2. One Battle After Another (2025) 一战再战 — 烂番茄 94% 观众 85% 豆瓣 8.0 — 86 个种子
>
> 暂无资源: GOAT (2026) — 可能仍在院线

## Step 4.5: 抓取用户评论

为有下载资源的电影抓取评论，帮助用户决定看什么。

**烂番茄电影详情页（首选，实测可用）：**

使用 WebFetch 抓取 `https://www.rottentomatoes.com/m/电影SLUG`，提取影评共识、烂番茄评分、观众评分、Top 3 用户评论。

URL slug 格式：电影名小写，空格替换为下划线。示例：sinners_2025、one_battle_after_another

如果 slug 不对（404），用 WebSearch "电影名 site:rottentomatoes.com" 找正确 URL。

**已确认不可用的评论来源（不要尝试）：**

- 豆瓣详情页 — 重定向到 sec.douban.com 反爬验证
- IMDb 评论页 — JS 渲染，返回空

**什么时候抓评论：**

- 搜索模式：抓当前搜索电影的评论
- 推荐模式：抓有资源的前 3-5 部电影的评论
- 不要对所有 15-20 部候选都抓，太慢

## Step 5: 字幕搜索（与 Step 3 并行执行，不要等用户要求）

**字幕搜索是标准流程的一部分，始终与种子搜索并行执行。** 在最终输出中一起展示字幕结果。

### Layer 1: WebFetch 字幕站（并行）

**SubtitleCat（首选，60+ 语言）：**

使用 WebFetch 抓取 SubtitleCat 搜索页面，提取所有可用语言和下载路径。

**SubHD（中文字幕首选）：**

使用 WebFetch 抓取 `https://subhd.tv/search/英文片名`，提取字幕列表。

### Layer 2: WebSearch 兜底

使用 WebSearch 搜索 "英文片名 年份 subtitles SRT 用户语言"。

### 已确认不可用的字幕站（不要尝试）：

- OpenSubtitles.org — WebFetch 返回 403
- SUBDL — WebFetch 返回 403
- 字幕库 zimuku.net — JS 重定向，WebFetch 无法解析

## Step 6: 格式化输出

将电影信息 + 种子结果 + 字幕信息 + 用户评论合并为清晰的输出。

用用户的语言输出。英文片名始终与本地片名一起展示，方便对照。

## 安全与权限

本 Skill 访问以下外部服务：

- apibay.org — TPB 种子搜索 API
- bitsearch.to — 种子搜索（HTML 爬取）
- torrentdownload.info — 种子搜索（HTML 爬取）
- yts.mx — YTS 种子 API（备选）
- rottentomatoes.com — 热门电影数据（HTML 爬取）
- movie.douban.com — 中文电影数据（HTML 爬取）
- subtitlecat.com — 字幕搜索（HTML 爬取）
- subhd.tv — 中文字幕搜索（HTML 爬取）
- torrentclaw.com — 种子聚合 API（仅在配置 key 时）
- api.themoviedb.org — 电影数据库 API（仅在配置 key 时）

本 Skill 不会：

- 下载任何种子文件或实际电影内容
- 修改系统设置或 ~/Documents/MovieMovie/ 以外的文件
- 向第三方发送用户数据
- 存储 API key（仅通过环境变量读取）
