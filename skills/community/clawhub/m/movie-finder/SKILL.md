# Movie Finder Skill

## 功能概述

- 搜索电影：按类型（科幻、喜剧、恐怖等）、年份、评分筛选
- 支持中英文关键词
- 展示电影海报、评分、简介、时长、导演、演员、类型标签
- 生成可播放的 HTML 页面，内嵌 iframe 播放器，支持多播放源页内切换
- 支持多结果列表，用户选择后生成播放页

> 安装说明见同目录 `INSTALL.md`。

---

## 触发词

| 场景 | 示例 |
|------|------|
| 按类型找片 | "想看一部科幻电影"、"recommend a comedy"、"恐怖片推荐" |
| 按年份找片 | "2024年科幻片"、"latest action movies"、"最近有什么好看的动作片" |
| 按评分找片 | "评分最高的科幻片"、"top rated thriller movies" |
| 按片名播放 | "搜一下《盗梦空间》"、"watch Inception online"、"盗梦空间在线看" |
| 仅查信息 | "这部电影讲什么"、"盗梦空间简介" |

## 意图解析

### 识别参数

| 参数 | 示例 | 提取方式 |
|------|------|----------|
| genre | 科幻、sci-fi、动作 | 关键词匹配（见下方类型映射表） |
| year | 2024、2025、"最新"、"最近" | 正则 `20\d{2}`；"最新/最近" → 当年 |
| rating | "评分最高"、"top rated"、"高分" | 关键词匹配 |
| keyword | 电影名、演员名 | 剩余文本 |
| intent | 播放 / 列表 / 仅信息 | 见下方意图分类 |

### 意图分类

1. **搜索播放**："想看[类型]"、"[电影名]在线看"、"watch [movie] online" → 搜索元数据 + 生成播放页
2. **筛选列表**："2024年科幻片"、"恐怖片推荐" → 返回列表，用户选一个再生成播放页
3. **仅搜索**："这部电影讲什么" → 只查元数据，不生成播放页

### 类型映射表

| 中文 | 英文 | TMDB genre_id |
|------|------|---------------|
| 科幻 | sci-fi / science fiction | 878 |
| 动作 | action | 28 |
| 喜剧 | comedy | 35 |
| 恐怖 | horror | 27 |
| 爱情 | romance | 10749 |
| 动画 | animation | 16 |
| 悬疑 | mystery | 9648 |
| 惊悚 | thriller | 53 |
| 冒险 | adventure | 12 |
| 奇幻 | fantasy | 14 |
| 剧情 | drama | 18 |
| 战争 | war | 10752 |
| 纪录片 | documentary | 99 |
| 犯罪 | crime | 80 |
| 家庭 | family | 10751 |

---

## 搜索策略

### 第一步：元数据搜索（TMDB API 优先）

TMDB（The Movie Database）提供完整的电影元数据。优先用 API 获取：

**搜索电影（按片名/关键词）：**
```
GET https://api.themoviedb.org/3/search/movie?api_key={KEY}&query={keyword}&language=zh-CN&page=1
```

**按类型 + 年份发现电影：**
```
GET https://api.themoviedb.org/3/discover/movie
  ?api_key={KEY}
  &language=zh-CN
  &sort_by=popularity.desc        # 或 vote_average.desc 按评分
  &with_genres={genre_id}         # 见类型映射表
  &primary_release_year={year}    # 可选
  &vote_average.gte={rating}      # 可选，评分筛选
  &page=1
```

**获取电影详情（含导演、演员、时长）：**
```
GET https://api.themoviedb.org/3/movie/{movie_id}?api_key={KEY}&language=zh-CN&append_to_response=credits
```

关键字段：
- `id` → TMDB ID（播放源需要）
- `imdb_id` → IMDb ID（部分播放源需要）
- `title` / `release_date` / `vote_average` / `runtime` / `overview`
- `poster_path` → 海报 URL：`https://image.tmdb.org/t/p/w500{poster_path}`
- `genres[].name` → 类型
- `credits.crew` 中 `job=Director` → 导演
- `credits.cast[].name` → 主演（取前 3-5 位）

> **API Key**：TMDB API 需要 key。若环境中无可用 key，降级到 web_search。

### 第一步（降级）：web_search 搜索元数据

无 API key 时，用 web_search 获取电影信息：

- 按片名：`{movie_name} 电影 简介 评分 年份`
- 按类型 + 年份：`{year}年 {genre} 电影 推荐 豆瓣` / `best {genre} movies {year}`
- 按类型 + 评分：`豆瓣 {genre} 高分电影` / `top rated {genre} movies`
- 获取 IMDb ID：`{movie_name} site:imdb.com`
- 获取 TMDB ID：`{movie_name} site:themoviedb.org`

从搜索结果中提取：片名、年份、评分、简介、海报图 URL、IMDb ID（格式 `tt\d{7,8}`）、TMDB ID。

### 第二步：构造播放源

拿到 IMDb ID 或 TMDB ID 后，按以下格式构造嵌入播放源 URL（无需额外 API）：

| 源名称 | URL 格式 | 标识类型 | 可靠性 |
|--------|----------|----------|--------|
| vidsrc | `https://vidsrc.net/embed/movie/{imdb_id}` | IMDb ID | ★★★★ |
| vidsrc.to | `https://vidsrc.to/embed/movie/{imdb_id}` | IMDb ID | ★★★★ |
| 2embed | `https://www.2embed.cc/embed/{imdb_id}` | IMDb ID | ★★★ |
| superembed | `https://multiembed.mov/?video_id={imdb_id}` | IMDb ID | ★★★ |
| vidsrc (TMDB) | `https://vidsrc.net/embed/movie?tmdb={tmdb_id}` | TMDB ID | ★★★ |

> 用 IMDb ID 优先（兼容性最好）。至少构造 2-3 个源，方便用户在播放页切换。

### 第三步：降级处理

- 若既无 TMDB API key、web_search 也未获取到 IMDb/TMDB ID：
  - web_search 搜索：`{movie_name} watch online free embed`
  - 从结果中直接提取可用的 embed URL
- 若所有方式均未找到播放源：返回电影信息 + 建议在 YouTube 等平台搜索

---

## 播放页生成

使用脚本 `scripts/generate_movie_page.py` 生成播放页（推荐），或直接用 HTML 模板。

### 方式一：脚本生成（推荐）

```bash
python scripts/generate_movie_page.py \
  --title "盗梦空间" \
  --year "2010" \
  --rating "8.8" \
  --plot "一个窃取梦境秘密的盗贼接到一项相反的任务..." \
  --poster "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg" \
  --runtime "148" \
  --director "克里斯托弗·诺兰" \
  --cast "莱昂纳多·迪卡普里奥, 约瑟夫·高登-莱维特" \
  --genres "科幻,动作,悬疑" \
  --sources '[{"name":"vidsrc","url":"https://vidsrc.net/embed/movie/tt1375666"},{"name":"2embed","url":"https://www.2embed.cc/embed/tt1375666"}]' \
  --output movie_inception.html
```

脚本特性：
- 用占位符替换（非 f-string）生成 HTML，CSS 花括号无需转义
- 多播放源页内切换（点击按钮在主播放器切换，无需跳转）
- 加载动画 + 8 秒超时兜底
- 海报加载失败时显示内置占位图（不依赖外部 placeholder 服务）
- HTML 转义防注入
- 响应式布局（移动端适配）
- 合规声明

### 方式二：直接写 HTML

如果无法调用脚本，直接将以下模板写入 `movie_{hash}.html`，替换 `__占位符__`：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ - 在线观看</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: linear-gradient(135deg, #0f0f1a 0%, #16213e 100%); color: #fff; font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; padding: 20px; min-height: 100vh; }
  .container { max-width: 1000px; margin: 0 auto; }
  .movie-info { display: flex; gap: 30px; margin-bottom: 25px; background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; flex-wrap: wrap; }
  .poster { flex: 0 0 220px; }
  .poster img { width: 100%; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
  .details { flex: 1; min-width: 280px; }
  .details h1 { font-size: 1.9em; margin-bottom: 12px; }
  .meta-row { display: flex; gap: 16px; margin-bottom: 14px; flex-wrap: wrap; align-items: center; }
  .rating-badge { background: rgba(245,197,24,0.15); color: #f5c518; padding: 4px 14px; border-radius: 20px; font-weight: bold; }
  .year-badge { background: rgba(255,255,255,0.1); padding: 4px 14px; border-radius: 20px; }
  .genres { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .genre-chip { background: rgba(255,255,255,0.08); padding: 3px 12px; border-radius: 15px; font-size: 0.82em; color: #aaa; }
  .plot { line-height: 1.8; color: #ccc; margin-bottom: 14px; }
  .player-wrapper { position: relative; padding-top: 56.25%; background: #000; border-radius: 12px; overflow: hidden; }
  .player-wrapper iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
  .src-btn { padding: 7px 18px; background: rgba(255,255,255,0.08); color: #aaa; border: none; border-radius: 6px; cursor: pointer; }
  .src-btn.active { background: #e50914; color: #fff; }
  .footer { text-align: center; margin-top: 35px; color: #666; font-size: 0.82em; }
</style>
</head>
<body>
<div class="container">
  <div class="movie-info">
    <div class="poster"><img src="__POSTER__" alt="__TITLE__"></div>
    <div class="details">
      <h1>__TITLE__</h1>
      <div class="meta-row">
        <span class="year-badge">__YEAR__</span>
        <span class="rating-badge">★ __RATING__</span>
        <span>⏱ __RUNTIME__ 分钟</span>
        <span>🎬 __DIRECTOR__</span>
      </div>
      <div class="genres">__GENRE_TAGS__</div>
      <p class="plot">__PLOT__</p>
      <p style="color:#aaa;font-size:0.9em;"><strong>主演：</strong>__CAST__</p>
    </div>
  </div>
  <div class="player-wrapper">
    <iframe id="playerFrame" src="__PRIMARY_SRC__" allowfullscreen></iframe>
  </div>
  <div style="margin:15px 0;display:flex;gap:8px;flex-wrap:wrap;">
    <button class="src-btn active" data-src="__SRC1__" onclick="switchSource(this)">源1</button>
    <button class="src-btn" data-src="__SRC2__" onclick="switchSource(this)">源2</button>
  </div>
  <div class="footer">播放源来自第三方，仅供学习交流，请支持正版</div>
</div>
<script>
  function switchSource(btn) {
    document.querySelectorAll('.src-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('playerFrame').src = btn.dataset.src;
  }
</script>
</body>
</html>
```

---

## 输出格式

### 1. 搜索结果列表（多条结果时）

```
🎬 找到以下电影：

1. 《{title}》({year}) ★{rating}
   {plot_short}

2. 《{title}》({year}) ★{rating}
   {plot_short}

...

请回复数字选择要播放的电影，或告诉我其他需求。
```

### 2. 直接播放（单条结果或用户选择后）

- 调用脚本或直接生成 HTML，写入 `movie_{hash}.html`
- 用 present_files 呈现给用户，告知可在浏览器中打开观看
- 文件输出到当前工作目录

### 3. 无播放源（找到信息但无可用源）

```
找到《{title}》({year})，但暂未找到可用播放源。

📖 电影信息：
- 评分：{rating}
- 类型：{genres}
- 简介：{plot}

💡 建议：可尝试在 YouTube 搜索 "{title} full movie"，或在正规流媒体平台观看。
```

---

## 注意事项

- **TMDB ID vs IMDb ID**：播放源常用 IMDb ID（`tt` 开头），部分支持 TMDB ID。搜索元数据时优先获取这两个 ID
- **封面图**：优先用 TMDB 图片 `https://image.tmdb.org/t/p/w500{poster_path}`
- **年份 "最新"**：优先搜索当年电影，TMDB 按 `primary_release_date.desc` 或 `popularity.desc` 排序
- **评分筛选**：TMDB `discover` 接口加 `vote_average.gte` 参数；web_search 时搜 "高分/豆瓣评分"
- **播放源失效**：第三方播放源域名会变动，若构造的 URL 无法播放，用 web_search 重新搜索当前可用源：`{movie_name} watch online embed {imdb_id}`
- **合规提示**：播放页底部已内置"播放源来自第三方，仅供学习交流，请支持正版"声明。推荐正版渠道时优先提及 YouTube、各大流媒体平台
- **网络问题**：播放源加载慢时耐心等待（播放页有加载动画 + 8 秒超时兜底），或切换备用源
