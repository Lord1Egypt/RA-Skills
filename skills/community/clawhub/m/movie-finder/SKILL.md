---
name: movie-finder
description: 搜索并播放电影。功能包括：(1) 按类型、年份、评分筛选电影；(2) 支持中英文输入；(3) 展示电影海报、评分、剧情简介；(4) 生成可点击的 iframe 播放页面，直接在线观看。触发场景包括：搜索电影、想看电影、找最新电影、按类型/年份/评分筛选电影。
---

# Movie Finder Skill

## 功能概述

- 搜索电影：按类型（科幻、喜剧、恐怖等）、年份、评分筛选
- 支持中英文关键词
- 展示电影海报、评分、简介、时长、导演、演员
- 生成可播放的 iframe 页面，点击即可观看
- 支持多结果列表，选择后播放

---

## 📥 安装说明

### 方式一：手动安装

1. 将本文件保存为 `SKILL.md`
2. 放入 `~/.openclaw/workspace/skills/movie-finder/` 目录
3. 目录结构：
   ```
   ~/.openclaw/workspace/skills/movie-finder/
   └── SKILL.md   ← 本文件
   ```
4. 重启 OpenClaw Gateway 使技能生效

### 方式二：通过 OpenClaw 命令行

```bash
# 确认 skills 目录存在
ls ~/.openclaw/workspace/skills/

# 创建 movie-finder 目录
mkdir -p ~/.openclaw/workspace/skills/movie-finder

# 写入 SKILL.md（直接复制本文件内容即可）
# 重启 Gateway
openclaw gateway restart
```

### 验证安装

安装完成后，在聊天中发送以下任一触发语验证：
- "我想看一部科幻电影"
- "最近有什么好看的动作片？"
- "搜一下《盗梦空间》"

---

## 意图解析

### 识别参数

| 参数 | 示例 | 提取方式 |
|------|------|----------|
| genre | 科幻、sci-fi、动作 | 关键词匹配 |
| year | 2024、2025、"最新" | 正则 `20\d{2}` 或 "最新/最新上映" |
| rating | "评分最高"、"top rated" | 关键词匹配 |
| keyword | 电影名、演员名 | 剩余文本 |

### 意图分类

1. **搜索播放**："想看[类型]"、"[电影名]在线看" → 搜索 + 播放
2. **筛选列表**："2024年科幻片"、"恐怖片推荐" → 返回列表，用户选一个再播放
3. **仅搜索**："这部电影讲什么" → 只查元数据，不播放

## 搜索策略

### 第一步：元数据搜索

优先使用 TMDB API 获取电影信息：

```
搜索关键词: TMDB API movie search
```

如果无法直接调 API，用 web_search 搜索：
- 电影详情：`{movie_name} site:themoviedb.org`
- 电影列表：`{genre} movies {year} site:themoviedb.org`
- 年份识别失败时搜：`latest {genre} movies 2025 site:themoviedb.org`

### 第二步：播放源搜索

搜索策略（优先级从高到低）：

1. **主流免费平台**（相对可靠）：
   - `site:2embed.ru`
   - `site:vidcloud.co`
   - `site:soap2day.rs`

2. **嵌入式播放**（常用）：
   - `{movie_name} full movie online free streaming iframe`
   - `{movie_name} watch online free embed`

3. **特定电影站**：
   - `{movie_name} streaming online free`

### 第三步：验证和选择

- 优先选择 `2embed` 或 `vidcloud` 类稳定源
- 如果搜索结果中多个源，选择第一个可用的
- 播放页 iframe src 格式：`https://{domain}/embed/{movie_id}` 或直接 `{url}`

## 播放页生成

生成一个独立的 HTML 页面，嵌入 iframe 播放源：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 在线观看</title>
<style>
  * { box-sizing: border-box; }
  body { background:#0f0f1a; color:#fff; font-family:'Segoe UI',Arial,sans-serif; margin:0; padding:20px; min-height:100vh; }
  .container { max-width:1000px; margin:0 auto; }
  .movie-header { display:flex; gap:30px; margin-bottom:25px; flex-wrap:wrap; }
  .poster { flex:0 0 220px; }
  .poster img { width:100%; border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.5); }
  .info { flex:1; min-width:280px; }
  .info h1 { margin:0 0 8px; font-size:2em; }
  .meta { color:#888; margin-bottom:12px; font-size:0.95em; }
  .meta span { margin-right:15px; }
  .rating { display:inline-flex; align-items:center; gap:6px; background:rgba(245,197,24,0.15); padding:6px 14px; border-radius:20px; margin-bottom:15px; }
  .rating .star { color:#f5c518; font-size:1.2em; }
  .rating .score { color:#f5c518; font-weight:bold; font-size:1.1em; }
  .genres { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:15px; }
  .genre { background:#2a2a4a; padding:4px 12px; border-radius:15px; font-size:0.85em; color:#aaa; }
  .plot { line-height:1.7; color:#ccc; margin-bottom:20px; }
  .cast { color:#888; font-size:0.9em; }
  .cast strong { color:#aaa; }
  .player-wrap { position:relative; width:100%; padding-top:56.25%; background:#000; border-radius:12px; overflow:hidden; margin-bottom:20px; }
  .player-wrap iframe { position:absolute; top:0; left:0; width:100%; height:100%; border:none; }
  .sources { display:flex; gap:10px; flex-wrap:wrap; margin-top:15px; }
  .source-btn { background:#e50914; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-size:0.9em; transition:background 0.2s; }
  .source-btn:hover { background:#ff1a1a; }
  .footer { text-align:center; color:#555; font-size:0.8em; margin-top:30px; }
</style>
</head>
<body>
<div class="container">
  <div class="movie-header">
    <div class="poster"><img src="{poster_url}" alt="{title}"></div>
    <div class="info">
      <h1>{title}</h1>
      <div class="meta"><span>{year}</span><span>{runtime}分钟</span><span>{director}</span></div>
      <div class="rating"><span class="star">★</span><span class="score">{rating}/10</span></div>
      <div class="genres">{genre_tags}</div>
      <p class="plot">{plot}</p>
      <p class="cast"><strong>主演：</strong>{cast}</p>
    </div>
  </div>
  <div class="player-wrap">
    <iframe src="{streaming_url}" allowfullscreen></iframe>
  </div>
  {alt_sources}
  <div class="footer">电影由墨子搜索整理，播放源来自第三方</div>
</div>
</body>
</html>
```

## 输出格式

1. **搜索结果列表**（多条时）：
   ```
   🎬 找到以下电影：
   
   1. [{title}] ({year}) ★{rating}
      {plot_short}
   
   2. ...
   
   请输入数字选择要播放的电影
   ```

2. **直接播放**（单条或用户选择后）：
   - 将 HTML 写入 `movie_{hash}.html`
   - 返回文件路径，告知用户可以直接在浏览器打开

3. **无播放源**：
   ```
   找到 [{title}]，但暂未找到免费播放源。
   
   📖 电影信息：
   {full_info}
   
   💡 建议：可尝试在 YouTube 或其他平台搜索 "{title} full movie"
   ```

## 播放源列表

| 源 | 格式 | 可靠性 |
|----|------|--------|
| 2embed.ru | `https://2embed.ru/embed/{tmdb_id}` | ★★★★ |
| vidcloud.co | `https://vidcloud.co/embed/?id={tmdb_id}` | ★★★ |
| vidsrc.me | `https://vidsrc.me/embed/{tmdb_id}` | ★★★★ |

> 注：播放源域名会变动，如果失效请用 web_search 重新搜索当前可用源

## 注意事项

- **TMDB ID**：播放源常用 TMDB ID（而非电影名），搜索元数据时优先获取 TMDB ID
- **封面图**：优先使用 TMDB 的 `https://image.tmdb.org/t/p/w500{poster_path}`
- **年份 "最新"**：优先搜索当年电影，TMDB 按 `primary_release_date.desc` 排序
- **评分筛选**：搜索时加 `vote_average.gte=8` 参数
- **网络问题**：播放源加载慢时耐心等待，或切换备用源
