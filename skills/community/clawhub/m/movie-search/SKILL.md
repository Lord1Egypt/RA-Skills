---
name: movie-search
description: 搜索电影/电视剧的下载和在线观看资源链接。当用户输入电影或电视剧片名（中文或英文，可附带年份），搜索各大资源网站并返回可用的下载链接和观看地址，按资源类型分组展示。触发条件：用户说"帮我找XXX的下载"、"XXX在哪里看"、"XXX有没有资源"、"搜索XXX电影"、"find movie"、"movie download"等，无论是否明确说"skill"都应使用本skill。
---

# 电影资源搜索

帮助用户找到电影/电视剧的下载资源和在线观看链接。

## 工作流程

### 第一步：解析输入

从用户输入中提取：
- **片名**（中文或英文）
- **年份**（可选，有助于精准匹配）
- **类型**：判断是电影还是电视剧（有"剧"、"季"、"season"、"series"等词，或知名剧集名称，则为剧集）

### 第二步：获取标准化片名

如果输入是中文片名，用 WebSearch 查询其英文原名：

```
搜索："[中文片名] English title year"
```

目标：英文原名 + 发行年份。如果是知名作品可直接从知识库获取，不必每次都搜索。

### 第三步：构造资源链接

#### 3a. YTS（高质量电影 BDRip）

YTS 专注于英语电影的高清 BDRip，不收录中文电影和电视剧。

- YTS 搜索页面：`https://yts.mx/browse-movies/{英文片名+年份（空格用+）}/all/all/0/latest/0/all`
- 直接链接示例：`https://yts.mx/movies/the-dark-knight-2008`

#### 3b. BT / 磁力下载站

**英文电影/剧集（国际站）：**
- 1337x：`https://1337x.to/search/{encode(英文片名 年份)}/1/`
- The Pirate Bay：`https://thepiratebay.org/search.php?q={encode(英文片名 年份)}`
- Torrent Galaxy：`https://torrentgalaxy.to/torrents.php?search={encode(英文片名)}`
- EZTV（剧集专用）：`https://eztv.re/search/{encode(英文片名)}`

**中文电影（国内站）：**
- 电影天堂：`https://s.dytt8.net/plus/search.php?q={encode(中文片名)}`
- BTDigg：`https://btdig.com/search?q={encode(中文片名)}`
- 磁力猫：`https://www.clicli.me/search?q={encode(中文片名)}`

#### 3c. 在线正版平台

**国内：**
- 爱奇艺：`https://www.iqiyi.com/search?para={encode(中文片名)}`
- 腾讯视频：`https://v.qq.com/x/search/?q={encode(中文片名)}`
- 优酷：`https://www.youku.com/search_video/q_{encode(中文片名)}.html`
- B站：`https://search.bilibili.com/video?keyword={encode(中文片名)}`

**海外：**
- Netflix：`https://www.netflix.com/search?q={encode(英文片名)}`
- Amazon Prime：`https://www.amazon.com/s?k={encode(英文片名)}&i=instant-video`
- JustWatch（多平台聚合）：`https://www.justwatch.com/us/search?q={encode(英文片名)}`

#### 3d. 字幕

- OpenSubtitles：`https://www.opensubtitles.org/zh/search2/sublanguageid-chi/moviename-{encode(英文片名)}`
- SubHD：`https://subhd.tv/search/{encode(中文片名或英文片名)}`
- 字幕库：`https://www.zimuku.net/search?q={encode(中文片名或英文片名)}`

### 第四步：格式化输出

**输出模板：**

```markdown
## 🎬 《中文片名》（英文片名, 年份）[电影/剧集]

基本信息：导演/类型/评分等

---

### YTS 高清下载（英文电影适用）
- [YTS 搜索页面](https://yts.mx/...)

### BT / 磁力下载
| 站点 | 链接 | 说明 |
|------|------|------|
| 1337x | [搜索](https://1337x.to/...) | 推荐找合集 |
| EZTV | [搜索](https://eztv.re/...) | 剧集专用 ← 仅剧集显示 |
| 电影天堂 | [搜索](https://s.dytt8.net/...) | 中文电影 ← 仅中文电影显示 |
...

### 在线观看（国内）
| 平台 | 链接 |
|------|------|
...

### 在线观看（海外）
...

### 字幕
| 站点 | 链接 |
|------|------|
| OpenSubtitles | [搜索](https://www.opensubtitles.org/...) |
| SubHD | [搜索](https://subhd.tv/search/...) |
| 字幕库 | [搜索](https://www.zimuku.net/...) |

💡 搜索技巧：（如有针对性提示则写，如"加 complete 找合集"、"加 1080p 过滤"）
```

## 注意事项

- **URL 编码**：空格用 `+`，中文字符用 URL 编码（如 `黑暗骑士` → `%E9%BB%91%E6%9A%97%E9%AA%91%E5%A3%AB`）
- **英文名优先**：国际 BT 站按英文名索引，即使中文电影也要提供英文名链接
- **条件显示**：
  - 剧集：突出 EZTV，提供按季搜索链接（S01, S02...）
  - 中文电影：突出电影天堂、BTDigg 等国内站，YTS 说明覆盖有限
  - 英文电影：突出 YTS、1337x
- **搜索技巧**：电视剧整季搜索加 `S01`；找合集加 `complete`；筛选画质加 `1080p`
- **相关内容**：如有知名前传/续集/系列，在末尾提及
