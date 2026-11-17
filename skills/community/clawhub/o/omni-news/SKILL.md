# Omni News — 多平台全方位新闻信息平台 v3.0

> 聚合央视新闻联播、国内权威媒体、国际财经、AI/科技、社交媒体热点（微博/知乎/小红书/抖音/快手/贴吧/虎扑/B站）、全球20国头条、X/YouTube Builder动态、实时热搜榜单。全部免费源，零 API key 依赖。

## 触发条件

用户提到以下任意关键词时触发：`新闻`、`日报`、`早报`、`快讯`、`头条`、`联播`、`财经`、`股市`、`AI动态`、`科技新闻`、`华尔街见闻`、`news`、`daily`、`今天有什么新闻`、`舆情`、`sentiment`。

> ⚠️ 触发词已收窄：移除了"最新"、"热点"、"热搜"、"builder"等过于宽泛的词汇，避免在无关对话中意外激活。仅当用户明确表达新闻/日报/快讯等具体意图时才触发。

## 数据与隐私

本技能在运行时可能调用以下第三方服务：

| 类型 | 服务 | 传输内容 | 用户控制 |
|------|------|---------|---------|
| 数据采集 | 微博/知乎/抖音/60s API/DailyHotApi | 无（仅获取公开热榜） | 可禁用 |
| 新闻源 | BBC/Reuters/华尔街见闻等RSS | 无 | 可禁用 |
| 搜索引擎 | web_search (bocha/baidu) | 用户查询关键词 | 可禁用 |
| 本地存储 | memory/*.md | 日报存档 | 可配置保留期 |

- **不收集**：用户身份、IP地址、搜索历史
- **不传输**：任何用户数据到技能开发者
- **本地存档**：默认保留30天，高热度事件永久保留；可通过设置调整
- **推送渠道**：仅在用户明确配置后启用，不会自动激活

## 数据保留策略

| 数据类型 | 保留期 | 说明 |
|---------|--------|------|
| 日报存档 | 30天 | 自动清理，可配置延长 |
| 高热度事件 | 永久 | 热度>1000万的事件长期保留 |
| 趋势图表 | 90天 | 用于趋势分析 |
| 搜索查询 | 不保留 | 即时处理，不存储 |

- 用户可随时手动清理所有本地存档
- 不向任何外部服务传输用户兴趣画像
- 所有数据仅存储在用户本地 workspace

---

## 架构：九层采集引擎 + 情感分析层

```
┌──────────────────────────────────────────────────────────────────────┐
│                         用户请求                                      │
└────────────────────────────┬─────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  引擎1:  新闻联播直采 (tv.cctv.com, 零依赖Python)                    │
│  引擎2:  国内权威媒体 (新浪/人民网/澎湃/36kr/IT之家/量子位等)         │
│  引擎3:  社交媒体热点 (微博/知乎/雪球 via Hotspot API)               │
│  引擎4:  国际财经 (WallstreetCN + Yahoo Finance + The Hear 20国)     │
│  引擎5:  国际新闻RSS (BBC/Reuters/Guardian/TechCrunch等21源)         │
│  引擎6:  AI/Builder动态 (Follow Builders 26人 + InBrief 100源)       │
│  引擎7:  搜索引擎交叉验证 (bocha + baidu 双引擎)                     │
│  引擎8:  60s API (微博/知乎/抖音/小红书/B站/头条/百度/猫眼)          │
│  引擎9:  DailyHotApi (40+平台: 快手/贴吧/虎扑/V2EX/地震等)           │
│  情感层: 中文情感分析 (BERT微调 + 多模型融合)                        │
└──────────────────────────────────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  处理层: 去重 → 信源分级 → 可信度标注 → 情感分析 → 影响分析         │
└──────────────────────────────────────────────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│  输出层: 结构化 Markdown 报告 + 存档 + 趋势图表                     │
└──────────────────────────────────────────────────────────────────────┘
```

> 架构已从10引擎精简为9引擎，移除了TrendRadar监控推送引擎（功能越界风险）。
> 推送功能仅在用户明确配置后启用，不会自动激活。

---

## 引擎1: 新闻联播直采（零依赖）

**数据源**: `https://tv.cctv.com/lm/xwlb/day/YYYYMMDD.shtml`
**脚本**: `scripts/fetch_xwlb.py`
**费用**: 完全免费

```bash
python3 scripts/fetch_xwlb.py [YYYYMMDD] [输出目录]
```

- 19:00 播出，约 20:00-20:30 文字稿全量上线
- 典型产出: 13-26 条，含全文 12-18 条

---

## 引擎2: 国内权威媒体（14个免费源）

### 2A: 新闻门户首页（web_fetch）

| 源 | URL | 类别 |
|----|-----|------|
| 人民网 | `https://www.people.com.cn` | 综合官方 |
| 中国新闻网 | `https://www.chinews.com` | 综合官方 |
| 新浪新闻 | `https://news.sina.com.cn` | 综合门户 |
| 澎湃新闻 | `https://www.thepaper.cn` | 深度报道 |
| IT之家 | `https://www.ithome.com` | 科技 |
| 量子位 | `https://www.qbitai.com` | AI |
| 机器之心 | `https://www.jiqizhixin.com` | AI |
| 36氪 | `https://36kr.com` | 科技与创投 |

### 2B: RSS 源

| 源 | RSS URL | 类别 |
|----|---------|------|
| 36氪 | `https://36kr.com/feed` | 科技创投 |
| 新华网 | `http://www.news.cn/rss/politics.xml` | 政治 |
| 央视 | `http://news.cctv.com/rss/china.xml` | 国内 |

### 2C: 实时新闻流

| 源 | URL | 方式 |
|----|-----|------|
| 新浪财经 7×24 | `https://finance.sina.com.cn/7x24/?tag=0` | web_fetch (maxChars:15000) |
| 财联社电报 | `https://www.cls.cn/telegraph` | browser |
| AIHOT | `https://aihot.virxact.com/daily` | AI 行业聚合 |

---

## 引擎3: 社交媒体热点（免费）

### 3A: Hotspot API（推荐，零 Key）

```bash
TIME_STEMP="$(TZ=Asia/Shanghai date +%Y-%m-%dT%H:%M)"
curl -s "https://hotspot.api4claw.com/hotspots/latest?timestamp=$TIME_STEMP"
```

- 返回 JSON: `source/source_name/items[]`
- 内置源: `xwlb` `weibo` `zhihu` `qqMorningPost`
- 按预估点击率排序 Top 10
- **完全免费，无需注册**

### 3B: 雪球

```
https://xueqiu.com — 个股讨论、热点新闻聚合
```

### 3C: X/Twitter（间接覆盖）

| 方式 | URL | 费用 |
|------|-----|------|
| web_search | `site:x.com 关键词` | 免费 |
| twikit | Python `pip install twikit` | 免费（需cookies） |
| Nitter 镜像 | 不稳定，已大量死亡 | 免费 |

**twikit 示例**（需先登录 cookies）:
```python
import asyncio
from twikit import Client
client = Client('en-US')
# await client.login(...)  # 首次需登录
tweets = await client.search_tweet('AI', 'Latest')
```

> X 官方 API 已付费（$200/月起），不建议使用。

---

## 引擎4: 国际财经（5个源，全部免费）

### 4A: WallstreetCN API（零 Key）

| 类型 | URL |
|------|-----|
| 最新 | `https://api-one-wscn.awtmt.com/apiv1/content/information-flow?channel=global&accept=article&limit=10` |
| 头条 | `https://api-one-wscn.awtmt.com/apiv1/content/carousel/information-flow?channel=global&limit=10` |
| 热文 | `https://api-one-wscn.awtmt.com/apiv1/content/articles/hot?period=all` |
| 搜索 | `https://api-one-wscn.awtmt.com/apiv1/search/article?query=关键词&limit=10` |

### 4B: Yahoo Finance API（零 Key）

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d"
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/%5EIXIC?interval=1d&range=1d"
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=1d"
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/CL=F?interval=1d&range=1d"
```

### 4C: The Hear（全球20国头条，零 Key）

```
GET https://www.thehear.org/api/country-view/[country]
```

- 支持: us, uk, germany, france, japan, korea, brazil, india, israel, russia, turkey 等20国
- 支持历史快照（`?at=YYYY-MM-DDTHH:MM:SSZ`）
- 支持7天日汇总（`?call=daily-overviews&from=...&to=...`）
- **完全免费**

### 4D: NewsMCP REST API（零 Key，事件聚合）

```
GET https://newsmcp.io/v1/news/?topics=technology&geo=europe&hours=24
```

- **12 个话题**: politics, economy, technology, science, health, environment, sports, culture, crime, military, education, society
- **30 个地区**: 6大洲24国
- AI 自动聚合同一事件的多源报道
- 按 source_count / impact_score 排序
- 完全免费，无需注册
- 返回: `{events: [{id, summary, topics, geo, entries_count, sources_count, impact_score, entries: [{title, url, domain, published_at}]}]}

```bash
# 全球科技新闻
curl -s "https://newsmcp.io/v1/news/?topics=technology&hours=24" | jq

# 美国政治
curl -s "https://newsmcp.io/v1/news/?topics=politics&geo=united+states&hours=48" | jq

# 事件详情
curl -s "https://newsmcp.io/v1/news/{event_id}/" | jq

# 列出所有话题/地区
curl -s "https://newsmcp.io/v1/news/topics/" | jq
curl -s "https://newsmcp.io/v1/news/regions/" | jq
```

---

## 引擎5: 国际新闻 RSS（21个源，全部免费）

### 5A: 综合国际新闻

| 源 | RSS URL | 语言 |
|----|---------|------|
| BBC | `http://feeds.bbci.co.uk/news/world/rss.xml` | 英文 |
| Reuters | `https://feeds.reuters.com/Reuters/worldNews` | 英文 |
| AP | `https://rsshub.app/apnews/topics/world-news` | 英文 |
| The Guardian | `https://www.theguardian.com/world/rss` | 英文 |
| Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` | 英文 |
| NPR | `https://feeds.npr.org/1001/rss.xml` | 英文 |
| DW | `https://rss.dw.com/rdf/rss-en-all` | 英文 |
| 南华早报 | `https://www.scmp.com/rss/91/feed` | 英文 |

### 5B: 科技/AI

| 源 | RSS URL | 类别 |
|----|---------|------|
| TechCrunch | `https://techcrunch.com/feed/` | 科技创投 |
| The Verge | `https://www.theverge.com/rss/index.xml` | 科技 |
| New Atlas | `https://newatlas.com/feed/` | 科技 |

### 5C: 科技巨头官方动态

| 源 | URL | 类别 |
|----|-----|------|
| OpenAI | `https://openai.com/news` | AI |
| Anthropic | `https://www.anthropic.com/news` | AI |
| Microsoft Source | `https://news.microsoft.com/source/feed/` | 科技 |
| Microsoft Blog | `https://blogs.microsoft.com/feed/` | 科技 |
| NVIDIA Blog | `https://blogs.nvidia.com/feed/` | AI/芯片 |
| NVIDIA News | `https://nvidianews.nvidia.com/news/rss.xml` | AI/芯片 |

### 5D: 开发者/科技社区

| 源 | URL | 方式 |
|----|-----|------|
| HackerNews | `https://hacker-news.firebaseio.com/v0/topstories.json` | API |
| ProductHunt | `https://www.producthunt.com/feed` | RSS |

---

## 引擎6: AI/Builder 动态（GitHub 发现，免费）

### 6A: Follow Builders（26位 AI Builder + 6个 YouTube 播客）

**项目**: https://github.com/zarazhangrui/follow-builders (6.7k stars)
**费用**: 完全免费，无 API key

**追踪的 26 位 AI Builder（X/Twitter）**:
Andrej Karpathy, Swyx, Josh Woodward, Boris Cherny, Thibault Sottiaux, Peter Yang, Nan Yu, Madhu Guru, Amanda Askell, Cat Wu, Thariq, Google Labs, Amjad Masad, Guillermo Rauch, Alex Albert, Aaron Levie, Ryo Lu, Garry Tan, Matt Turck, Zara Zhang, Nikunj Kothari, Peter Steinberger, Dan Shipper, Aditya Agarwal, Sam Altman, Claude

**6 个 YouTube 播客**:
Latent Space, Training Data, No Priors, Unsupervised Learning, The MAD Podcast, AI & I

**2 个官方博客**:
Anthropic Engineering, Claude Blog

**使用方法**:
```bash
git clone https://github.com/zarazhangrui/follow-builders.git ~/skills/follow-builders
# 技能会自动从中央 feed 获取最新内容
```

### 6B: InBrief.info（100 个 AI 信源）

**项目**: https://github.com/frankzch/ai-news-skill
**费用**: Guest 3条/请求，注册免费用户 6条/请求，会员 100条/请求

**覆盖范围**:
- 20 个新闻源: TechReview, TheVerge AI, Venturebeat, TechCrunch, Nvidia Blog, Apple AI, Microsoft Blog, Google Deepmind, OpenAI, HuggingFace 等
- 60 个社媒热点: Reddit, X, HackerNus
- 18 个 YouTube AI 创作者: Matt Wolfe, Dwarkesh Patel, DataDrivenNYC, Latent Space 等
- GitHub Trending AI 仓库

```bash
# 无需 key，guest 模式
curl -s "https://inbrief.info/api/v1/news?category=news&hours=24"
# 返回 JSON，guest 限制 3 条/请求
```

### 6C: AI News Digest（60+ 信源，5 道 QA Gate）

**项目**: https://github.com/chengjialu8888/AI_News_Digest
**费用**: 完全免费

**特色**:
- 微信公众号全文抓取（mp.weixin.qq.com → Markdown 归档）
- 5 道质量审核: 去重→交叉验证→信号分级→事实核验→完整性自检
- 12 列 CSV 输出
- 9 层信源系统（中文核心+英文一手+数据型+Builder+趋势研究+微信生态+agents-radar MCP+AI HOT Feed）

---

## 引擎7: 搜索引擎（双引擎交叉验证）

| 引擎 | 用途 | 费用 |
|------|------|------|
| web_search(channel="bocha") | 全量搜索 | 免费 |
| web_search(channel="baidu") | 验证含数据条目 | 免费 |
| Bing CN | 备用搜索 | 免费 |

---

## 引擎8: ⭐NEW — 60s API（实时热搜全平台覆盖）

**项目**: https://github.com/vikiboss/60s (5.8k stars)
**费用**: 完全免费，无需 API key
**文档**: https://docs.60s-api.viki.moe
**公共实例**: `https://60s.viki.moe`（也可 Docker 自部署）

### 8A: 热门榜单（核心，零 Key）

> ⚠️ 实测验证状态（2026-09-17）：公共实例 `60s.viki.moe` 部分端点返回 404。
> 下表标注实测结果，未验证端点标注来源为文档声明。

| 端点 | 说明 | 状态 |
|------|------|------|
| `GET /v2/weibo` | 微博热搜 | ✅ 实测可用 |
| `GET /v2/zhihu` | 知乎话题榜 | ✅ 实测可用（30条） |
| `GET /v2/douyin` | 抖音热搜 | ✅ 实测可用（50条） |
| `GET /v2/bilibili` | 哔哩哔哩热搜 | ✅ 实测可用（50条） |
| `GET /v2/toutiao` | 头条热搜榜 | ✅ 实测可用（50条） |
| `GET /v2/maoyan` | 猫眼全球票房总榜 | ✅ 实测可用（data.list） |
| `GET /v2/xiaohongshu` | 小红书热点 | ❌ 返回404（自部署可用） |
| `GET /v2/baidu` | 百度实时热搜 | ❌ 返回null |
| `GET /v2/baidutop` | 百度电视剧榜 | 📝 文档声明 |
| `GET /v2/baidutieba` | 百度贴吧话题榜 | 📝 文档声明 |
| `GET /v2/ithome` | IT之家热门 | ❌ 返回404 |
| `GET /v2/kuaishou` | 快手热点 | 📝 文档声明 |
| `GET /v2/quark` | 夸克热点 | 📝 文档声明 |
| `GET /v2/dongchedi` | 懂车帝热搜 | 📝 文档声明 |
| `GET /v2/wangyi` | 网易云榜单 | 📝 文档声明 |
| `GET /v2/hackernews` | Hacker News 热帖 | 📝 文档声明 |
| `GET /v2/maoyan-tv` | 猫眼电视收视排行 | 📝 文档声明 |
| `GET /v2/maoyan-web` | 猫眼网剧实时热度 | 📝 文档声明 |
| `GET /v2/douban-movie` | 豆瓣全球口碑电影榜 | 📝 文档声明 |
| `GET /v2/douban-tv` | 豆瓣全球口碑剧集榜 | 📝 文档声明 |

```bash
# 微博热搜（实测可用）
curl -s "https://60s.viki.moe/v2/weibo" | jq

# 抖音热搜（实测可用，返回50条）
curl -s "https://60s.viki.moe/v2/douyin" | jq

# 知乎话题榜（实测可用，返回30条）
curl -s "https://60s.viki.moe/v2/zhihu" | jq

# 头条热搜（实测可用，返回50条）
curl -s "https://60s.viki.moe/v2/toutiao" | jq

# B站热搜（实测可用，返回50条）
curl -s "https://60s.viki.moe/v2/bilibili" | jq

# 猫眼票房（实测可用）
curl -s "https://60s.viki.moe/v2/maoyan" | jq '.data.list'
```

### 8B: 周期资讯

| 端点 | 说明 | 状态 |
|------|------|------|
| `GET /v2/60s` | 每天60秒读懂世界（精选15条+微语） | ✅ 实测可用 |
| `GET /v2/60s?encoding=text` | 纯文本格式 | ✅ 实测可用 |
| `GET /v2/60s?encoding=image` | 原图直链 | 📝 文档声明 |
| `GET /v2/ai` | AI 资讯快报 | 📝 文档声明 |
| `GET /v2/bing` | 必应每日壁纸 | 📝 文档声明 |
| `GET /v2/exchange` | 当日货币汇率 | 📝 文档声明 |
| `GET /v2/history` | 历史上的今天 | ❌ 返回404 |
| `GET /v2/epic` | Epic 免费游戏 | 📝 文档声明 |
| `GET /v2/it` | 实时 IT 资讯 | 📝 文档声明 |

```bash
# 60秒读世界（推荐，高质量精选）
curl -s "https://60s.viki.moe/v2/60s" | jq

# AI 资讯快报
curl -s "https://60s.viki.moe/v2/ai" | jq
```

### 8D: 自部署（推荐生产环境）

```bash
# Docker 一键部署（固定版本，避免供应链风险）
docker run -d --restart always --name 60s -p 4399:4399 vikiboss/60s:2.1.0
# 验证镜像签名：docker trust inspect vikiboss/60s:2.1.0
```

> ⚠️ 公共实例 `60s.viki.moe` 每日额度有限，生产环境建议自部署。

---

## 引擎9: ⭐NEW — DailyHotApi（40+平台聚合API）

**项目**: https://github.com/imsyy/DailyHotApi (4.1k stars)
**费用**: 完全免费，支持 JSON + RSS 双模式
**在线实例**: `https://api-hot.imsyy.top`

### 9A: 完整平台列表（40+）

| 平台 | 调用名称 | 类别 |
|------|---------|------|
| 哔哩哔哩 | bilibili | 视频 |
| AcFun | acfun | 视频 |
| 微博 | weibo | 社交 |
| 知乎 | zhihu | 社交 |
| 知乎日报 | zhihu-daily | 社交 |
| 百度 | baidu | 搜索 |
| 抖音 | douyin | 短视频 |
| ⭐ 快手 | kuaishou | 短视频 |
| 豆瓣电影 | douban-movie | 影视 |
| 豆瓣小组 | douban-group | 社交 |
| 百度贴吧 | tieba | 论坛 |
| 少数派 | sspai | 科技 |
| IT之家 | ithome | 科技 |
| IT之家喜加一 | ithome-xijiayi | 科技 |
| 简书 | jianshu | 写作 |
| 果壳 | guokr | 科学 |
| 澎湃新闻 | thepaper | 新闻 |
| 今日头条 | toutiao | 新闻 |
| 36氪 | 36kr | 科技创投 |
| 51CTO | 51cto | 技术 |
| CSDN | csdn | 技术 |
| NodeSeek | nodeseek | 主机 |
| 稀土掘金 | juejin | 技术 |
| 腾讯新闻 | qq-news | 新闻 |
| 新浪网 | sina | 门户 |
| 新浪新闻 | sina-news | 新闻 |
| 网易新闻 | netease-news | 新闻 |
| 吾爱破解 | 52pojie | 安全 |
| 全球主机交流 | hostloc | 主机 |
| 虎嗅 | huxiu | 科技 |
| 酷安 | coolapk | 安卓 |
| 虎扑 | hupu | 体育 |
| 爱范儿 | ifanr | 科技 |
| 英雄联盟 | lol | 游戏 |
| 米游社 | miyoushe | 游戏 |
| 原神 | genshin | 游戏 |
| 崩坏3 | honkai | 游戏 |
| 崩坏星穹铁道 | starrail | 游戏 |
| 微信读书 | weread | 阅读 |
| NGA | ngabbs | 论坛 |
| V2EX | v2ex | 技术 |
| HelloGitHub | hellogithub | 开源 |
| 中央气象台 | weatheralarm | 气象 |
| ⭐ 中国地震台 | earthquake | 应急 |
| 历史上的今天 | history | 科普 |

### 9B: 调用方式

```bash
# JSON 模式
curl -s "https://api-hot.imsyy.top/weibo" | jq
curl -s "https://api-hot.imsyy.top/douyin" | jq
curl -s "https://api-hot.imsyy.top/zhihu" | jq
curl -s "https://api-hot.imsyy.top/baidu" | jq
curl -s "https://api-hot.imsyy.top/toutiao" | jq
curl -s "https://api-hot.imsyy.top/bilibili" | jq
curl -s "https://api-hot.imsyy.top/kuaishou" | jq
curl -s "https://api-hot.imsyy.top/tieba" | jq
curl -s "https://api-hot.imsyy.top/hupu" | jq
curl -s "https://api-hot.imsyy.top/ithome" | jq
curl -s "https://api-hot.imsyy.top/36kr" | jq
curl -s "https://api-hot.imsyy.top/thepaper" | jq

# RSS 模式（将路径改为 /rss）
curl -s "https://api-hot.imsyy.top/rss/weibo" | head -50
```

### 9C: 自部署

```bash
# Docker（固定版本，避免供应链风险）
docker pull imsyy/dailyhot-api:2.1.0
docker run --restart always -p 6688:6688 -d imsyy/dailyhot-api:2.1.0
# 验证镜像签名：docker trust inspect imsyy/dailyhot-api:2.1.0

# 或 Vercel / Railway / Zeabur 一键部署
```

---

## ~~引擎10: TrendRadar（已移除）~~

> ⚠️ **本引擎已从技能中移除。** TrendRadar的智能监控+推送功能超出了新闻日报的核心定位，且多渠道推送（企微/飞书/Telegram）扩大了数据流表面。如需监控功能，请使用独立的TrendRadar技能。

---

**项目**: https://github.com/sansan0/TrendRadar
**费用**: 完全免费，GitHub Pages 部署
**特性**: 11平台监控 + 关键词过滤 + 多渠道推送

### 10A: 监控平台（11个）

- 今日头条、百度热搜、华尔街见闻、澎湃新闻、bilibili、财联社、凤凰网、贴吧、微博、抖音、知乎

### 10B: API 接口

```bash
# JSON 格式热点数据
curl -s "https://your-domain/api/trends.json" | jq

# 图片版日报
curl -s "https://your-domain/img/news.jpg" --output news.jpg
```

### 10C: 核心特性

| 特性 | 说明 |
|------|------|
| 智能推送策略 | 投资者(incremental) / 自媒体(current) / 普通用户(daily) |
| 关键词过滤 | 设置个人关键词（如 AI、比亚迪），只推送相关热点 |
| 静默推送 | 时间窗口控制（如 9:00-18:00） |
| 多渠道推送 | 企业微信、飞书、钉钉、Telegram |
| 热点词汇统计 | 自动统计关键词出现频率和平台分布 |
| GitHub Actions | 自动化运行，无需服务器 |

### 10D: 部署

```bash
# Fork 仓库 → Settings → Pages → 启用
# 或 Docker 部署
```

---

## 情感分析层: ⭐NEW — 中文情感分析

### 工具1: BettaFish 方法论（微舆，42.2k stars）

**项目**: https://github.com/666ghj/BettaFish
**定位**: 多Agent舆情分析系统（方法论提取，非直接安装）

**可提取的方法论**:
1. **多Agent协作**: Query Agent(搜索) + Media Agent(多模态) + Insight Agent(数据库) + Report Agent(报告)
2. **论坛协作机制**: Agent间辩论+链式思维碰撞，避免单一模型局限
3. **情感分析模型**: 微调BERT/GPT-2 LoRA模型，专门针对微博情感
4. **5类Agent工具集**: 每类Agent有独特工具集+思维模式+反思机制
5. **公私域数据融合**: 公开舆情 + 内部业务数据库联合分析

**注意**: BettaFish 需要 PostgreSQL + LLM API + Docker，重量级部署。建议仅提取方法论。

### 工具2: 中文金融新闻情感分析（17 stars）

**项目**: https://github.com/wangy8989/Chinese-Financial-News-Sentiment-Analysis
**费用**: 完全免费
**模型**: RNN / LSTM / BERT (Chinese RoBERTa-Base)
**数据**: 提供 Train_Data.csv + Test_Data.csv + 情感词典

```python
# 使用示例
from models import BertForSentiment
model = BertForSentiment.from_pretrained("hfl/chinese-roberta-wwm-ext")
# 预测: 正面 / 负面
```

### 工具3: 轻量级情感分析（无需模型训练）

```python
# 方案A: 使用 SnowNLP（中文情感分析库）
# pip install snownlp
from snownlp import SnowNLP
s = SnowNLP("这个产品真的很不错")
print(s.sentiments)  # 0.0~1.0，>0.6 正面，<0.4 负面

# 方案B: 使用百度飞桨 PaddleNLP（预训练模型）
# pip install paddlenlp
from paddlenlp import Taskflow
senta = Taskflow("sentiment_analysis")
print(senta("这个产品真的很不错"))
# [{'label': 'positive', 'score': 0.99}]
```

### 情感分析集成策略

| 场景 | 方案 | 费用 |
|------|------|------|
| 实时热点情感 | SnowNLP 批量分析 | 免费 |
| 金融新闻情感 | BERT 微调模型 | 免费（需训练） |
| 社媒评论情感 | PaddleNLP 预训练 | 免费 |
| 深度舆情报告 | BettaFish 方法论 | 需部署 |

---

## 社交媒体覆盖（v3.0 全面升级）

| 平台 | 状态 | 来源 |
|------|------|------|
| **微博** | ✅ 直接覆盖 | Hotspot API + 60s API(实测) + DailyHotApi |
| **知乎** | ✅ 直接覆盖 | Hotspot API + 60s API(实测) + DailyHotApi |
| **腾讯早报** | ✅ 直接覆盖 | Hotspot API |
| **抖音** | ✅ **直接覆盖** | **60s API `/v2/douyin`(实测50条)** + DailyHotApi |
| **B站** | ✅ 直接覆盖 | 60s API(实测50条) + DailyHotApi |
| **今日头条** | ✅ **直接覆盖** | **60s API `/v2/toutiao`(实测50条)** + DailyHotApi |
| **百度热搜** | ⚠️ 文档可用 | 60s API(公共实例返回null，自部署可用) + DailyHotApi |
| **小红书** | ⚠️ 间接 | 60s API 公共实例返回404（自部署可用），web_search 间接覆盖 |
| **快手** | ⚠️ 文档可用 | DailyHotApi（60s API 文档声明但待验证） |
| **贴吧** | ⚠️ 文档可用 | DailyHotApi + 60s API（文档声明） |
| **虎扑** | ⚠️ 文档可用 | DailyHotApi |
| **懂车帝** | ⚠️ 文档可用 | 60s API（文档声明） |
| **IT之家** | ⚠️ 文档可用 | 60s API（公共实例返回404）+ DailyHotApi |
| **猫眼票房** | ✅ **直接覆盖** | **60s API `/v2/maoyan`(实测)** |
| **豆瓣** | ⚠️ 文档可用 | 60s API（文档声明）+ DailyHotApi |
| **雪球** | ✅ 直接覆盖 | web_fetch |
| **地震速报** | ⚠️ 文档可用 | DailyHotApi |
| **气象预警** | ⚠️ 文档可用 | DailyHotApi |
| **HackerNews** | ✅ 直接覆盖 | Firebase API |
| **X/Twitter** | ⚠️ 间接 | web_search + twikit + Follow Builders + InBrief |
| **YouTube** | ⚠️ 间接 | Follow Builders 6个播客 + web_search |
| **Reddit** | ⚠️ 间接 | InBrief + web_search |
| **ProductHunt** | ✅ 直接覆盖 | RSS |

> **图例**: ✅ 实测可用 | ⚠️ 文档声明/待验证 | ❌ 不可用 | 间接=通过搜索覆盖

---

## 完整免费源清单（80+）

### 国内（25个）
1. CCTV 新闻联播（脚本直采）
2. 人民网 / 中国新闻网
3. 新浪新闻 + 财经 7×24
4. 澎湃新闻
5. IT之家 / 量子位 / 机器之心
6. 36氪（RSS+首页）
7. AIHOT
8. 财联社电报
9. Hotspot API（微博+知乎+腾讯早报+新闻联播）
10. 雪球
11. 新华网 RSS
12. 央视 RSS
13. ⭐ 60s API（微博/知乎/抖音/小红书/B站/头条/百度/猫眼/豆瓣/IT之家/贴吧/懂车帝/快手）
14. ⭐ DailyHotApi（快手/贴吧/虎扑/V2EX/地震/气象/历史/酷安/51CTO/NGA/微信读书等）

> 移除了TrendRadar（监控+推送功能超出新闻日报核心定位）

### 国际（21个）
16. WallstreetCN API（4端点）
17. Yahoo Finance API
18. The Hear（20国）
19. NewsMCP（事件聚合，12话题30地区）
20. BBC / Reuters / AP / Guardian / Al Jazeera / NPR / DW RSS
21. 南华早报 RSS
22. TechCrunch / TheVerge / NewAtlas RSS
23. OpenAI / Anthropic 官方
24. Microsoft / NVIDIA 官方 RSS
25. HackerNews API
26. ProductHunt RSS

### AI/Builder（GitHub 发现，15个）
27. Follow Builders（26位 X Builder）
28. Follow Builders（6个 YouTube 播客）
29. Anthropic Engineering Blog
30. Claude Blog
31. InBrief.info（100 AI 信源）
32. AI News Digest（60+ 信源 + 微信全文抓取）
33. GitHub Trending（AI 仓库）

### 情感分析（3个）
34. SnowNLP（轻量级中文情感）
35. PaddleNLP（百度飞桨预训练模型）
36. BettaFish 方法论（多Agent舆情分析）

---

## 输出格式

### 标准日报模板

```markdown
# 📰 Omni News 日报 — YYYY-MM-DD
> 生成时间: YYYY-MM-DD HH:MM GMT+8
> 数据源: 新闻联播 + 新浪/财联社 + 微博/知乎/抖音/小红书/快手/B站 +
>          WallstreetCN + BBC/Reuters + 36氪/TechCrunch + NewsMCP +
>          InBrief + Follow Builders + 全球20国 + 60s API + DailyHotApi

## 📌 今日一句话总结
[40字以内概括]

---

## 🔥 全网热搜 Top 15（跨平台聚合）
> 数据源: 微博 + 抖音 + 小红书 + 知乎 + 百度 + 头条 + B站

1. **[标题]** — 一句话摘要 | 🔥热度: XX万 | 来源: 微博/抖音/小红书
2. ...

## 📊 平台热度排行
| 平台 | Top 1 | Top 2 | Top 3 |
|------|-------|-------|-------|
| 微博 | ... | ... | ... |
| 抖音 | ... | ... | ... |
| 小红书 | ... | ... | ... |
| 知乎 | ... | ... | ... |
| 百度 | ... | ... | ... |
| B站 | ... | ... | ... |

---

## 🌍 一、全球政治军事 (6-10条)
## 🇨🇳 二、中国政治军事 (6-10条)
## 💰 三、全球财经股市 (6-10条)
## 📈 四、中国财经股市 (6-10条)
## 🤖 五、AI 人工智能 (6-10条)
## 🔭 六、科技领域 (6-10条)
## 📱 七、消费电子 (6-10条)
## 🏠 八、白色家电 (6-10条)

## 🎙️ AI Builder 动态（Follow Builders）
### X/Twitter 精选
1. **[Builder名字]**: 一句话摘要 | [原文](链接)
### YouTube 播客更新
1. **[播客名]**: 一句话摘要

## 📰 海外 AI 媒体速览（InBrief 100源精选）
1. **[标题]** — 一句话摘要 | 来源

## 🌐 全球头条速览（The Hear 20国）
| 国家 | 头条 |
|------|------|
| 🇺🇸 美国 | ... |
| 🇬🇧 英国 | ... |
| 🇩🇪 德国 | ... |
| 🇯🇵 日本 | ... |
| 🇰🇷 韩国 | ... |

## 📺 新闻联播精选 (如有)
1. 【标题】一句话解读

## 🔗 NewsMCP 热门事件
1. **[事件摘要]** — 涉及 N 家媒体, 影响分 X/10

## 💭 舆情情感分析
| 话题 | 情感倾向 | 热度 |
|------|---------|------|
| ... | 🟢正面/🔴负面/🟡中性 | ⭐1-5 |

## ⚡ 实时快讯（60s API + DailyHotApi）
- 微博热搜 TOP 5
- 抖音热点 TOP 5
- 知乎话题 TOP 5

---
*可信度等级: 🔴官方确认 | 🟡专业媒体 | ⚪社交媒体/第三方*
```

### 快速简报模式（"快讯"/"简报"触发）

只输出 10 条核心（3:4:3 比例）:
- 📈 投资美股市场 Top 3
- 🌍 全球 AI 前沿 Top 4
- 🇨🇳 中国 AI 动态 Top 3

每条带热度评分（⭐1-5）和一句话影响分析。

### 舆情分析模式（"舆情"/"sentiment"触发）

输出:
1. 热点话题列表（跨平台）
2. 每个话题的情感倾向（SnowNLP/PaddleNLP）
3. 平台热度分布
4. 关键意见领袖(KOL)动态
5. 舆情趋势预测（基于 BettaFish 方法论）

### ⭐NEW 场景化早报模式（from cclank 项目）

| 场景 | 触发词 | 内容侧重 |
|------|--------|---------|
| 💰 财经早报 | "财经早报"/"市场早报" | 股市/汇率/黄金/油价/经济数据 |
| 🚀 科技早报 | "科技早报"/"Tech早报" | AI/芯片/消费电子/航天 |
| 🍉 吃瓜早报 | "吃瓜"/"热搜汇总" | 微博/抖音/小红书/贴吧热点 |
| 🤖 AI 深度日报 | "AI日报"/"AI动态" | 论文/模型/产品/Builder动态 |
| 🌍 国际新闻 | "国际新闻"/"全球头条" | 国际20国+BBC/Reuters |
| 📺 新闻联播摘要 | "联播摘要"/"CCTV" | 当日联播要点 |
| 🎙️ AI Builder 动态 | "Builder动态"/"X热点" | 26位Builder+6个播客 |
| 💭 舆情报告 | "舆情报告"/"热点分析" | 情感分析+趋势+平台分布 |

---

## ⭐NEW 信息反馈优化（v3.1 重大升级）

### 1. 去重与事件聚类（from TrendSonar + chronicle）

#### 1A: 多阶段去重流水线

```
原始采集 → 精确去重 → 语义去重 → 事件聚类 → 最终呈现
```

**阶段1: 精确去重**
- URL 完全一致 → 只保留一条
- URL 不同但标题完全一致 → 合并
- 使用 MD5/SHA256 对标题+内容做指纹比对

**阶段2: 语义去重（Embedding 相似度）**
```python
# 使用 SentenceTransformer 生成 Embedding
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode([item['title'] for item in news_items])

# 计算余弦相似度，阈值 0.85 以上视为同一事件
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(embeddings)

# 合并相似条目，保留信息最丰富的一条作为主条目
```

**阶段3: 事件聚类（from chronicle 项目）**
- 使用 MinHash LSH 做近似最近邻搜索
- HDBSCAN 聚类算法自动发现事件簇
- 最小聚类大小: 3 条（少于3条的聚类归为"其他"）
- 输出: 事件簇列表，每个簇包含多条新闻报道

**阶段4: AI 核验（from TrendSonar）**
- 对 Embedding 高相似度的候选对，用 LLM 做最终判断
- Prompt: "以下两条新闻是否报道同一事件？是/否。如果它们是不同的，用一句话说明区别。"
- 避免误合并

#### 1B: 事件数据结构

```json
{
  "event_id": "evt_20260917_001",
  "title": "事件标题（从多源中提炼）",
  "summary": "3句话事件概述",
  "sources": [
    {"name": "BBC", "title": "...", "url": "...", "published_at": "..."},
    {"name": "Reuters", "title": "...", "url": "...", "published_at": "..."},
    {"name": "新华网", "title": "...", "url": "...", "published_at": "..."}
  ],
  "source_count": 8,
  "platforms": ["BBC", "Reuters", "新华网", "36氪"],
  "first_seen": "2026-09-17T08:00:00",
  "last_updated": "2026-09-17T14:30:00",
  "sentiment": "neutral",
  "keywords": ["关键词1", "关键词2"],
  "impact_score": 7.5
}
```

#### 1C: 专题追踪（from TrendSonar）

- 自动从近期高热新闻中发现候选事件簇
- AI 审核生成专题（判断是否值得追踪）
- 专题时间轴: 按时间排列的关键节点
- 专题趋势仪表盘: 热度随时间变化
- 手动创建专题: 用户可指定关键词创建

### 2. 输出格式化模板（from cclank + TrendSonar）

#### 2A: 杂志级排版原则

1. **视觉层次清晰**: H1 → H2 → H3 递减，每屏不超过2个H2
2. **信息密度适中**: 每条新闻 2-4 行，不超过 150 字
3. **视觉锚点**: 每条新闻开头用 emoji 标记类别（🤖AI/💰金融/🌍国际/🇨🇳国内）
4. **来源标注**: 每条末尾标注来源和发布时间
5. **可信度分级**: 🔴官方确认 🟡专业媒体 ⚪社交媒体/第三方
6. **分隔线**: 大板块之间用 `---` 分隔
7. **表格用于对比**: 排行榜/多国对比用表格，故事叙述用列表

#### 2B: 日报头部模板

```markdown
# 📰 Omni News 日报 — YYYY-MM-DD (星期X)

> 🕐 生成时间: YYYY-MM-DD HH:MM GMT+8
> 📊 数据源: 82个平台 | 采集: XXX条 | 去重后: XXX条 | 聚类事件: XXX个
> 🔥 今日关键词: [关键词1] [关键词2] [关键词3]

## 📌 今日一句话
[30字以内概括当天最值得关注的事]

---
```

#### 2C: 新闻条目模板

```markdown
### 🤖 AI 人工智能

1. **[标题]** ⭐热度: 4.5/5
   > 2句话核心摘要。包含最关键的数据或事实。
   
   📎 来源: BBC / Reuters / 新华网 | 🕐 2小时前
   💭 情感: 🟢正面 | 关键词: GPT-5, 多模态, Agent

2. **[另一条新闻]** ⭐热度: 3/5
   > 摘要...
   
   📎 来源: 36氪 | 🕐 5小时前
   💭 情感: 🟡中性
```

#### 2D: 事件聚合展示模板

```markdown
### 🔥 热点事件聚合

#### 事件1: [标题] — 8家媒体报道
> 3句话事件概述。提炼多方观点的核心共识和分歧。

| 来源 | 角度 | 标题 |
|------|------|------|
| BBC | 国际视角 | ... |
| 新华网 | 官方立场 | ... |
| 36氪 | 产业分析 | ... |

📊 情感分布: 🟢正面 40% | 🟡中性 35% | 🔴负面 25%
📈 趋势: 上升中 | 首发: 6小时前
```

### 3. 个性化关键词追踪（from TrendSonar + cclank）

#### 3A: 关键词配置

用户可在对话中指定关注关键词:
```
"帮我关注 AI Agent 和 比亚迪 的新闻"
"今天有什么关于 英伟达 的消息？"
```

#### 3B: 追踪策略（from TrendSonar）

| 策略 | 说明 |
|------|------|
| 精确匹配 | 标题/内容包含关键词 |
| 语义匹配 | Embedding 相似度 > 0.7 |
| 关注关键词过滤 | 只推送包含关注关键词的新闻 |
| 权重调整 | 含关键词的新闻热度加权 |

#### 3C: 智能推送规则（from TrendSonar）

| 用户类型 | 推送策略 |
|---------|---------|
| 投资者 | 增量推送（只推新消息），关键词: 股市/汇率/黄金 |
| 自媒体 | 实时热点（当前最热），关键词: 热搜/爆款 |
| 普通用户 | 每日汇总，关键词: 用户自定义 |

### 4. 多格式输出（from cclank + TrendSonar）

#### 4A: Markdown（默认，聊天场景）

- 用于聊天对话直接展示
- 带完整格式和链接
- 适合快速阅读

#### 4B: HTML（邮件/分享场景）

```html
<!-- Omni News HTML邮件模板，参考自cclank开源项目 -->
<div style="max-width:600px;margin:0 auto;font-family:-apple-system,sans-serif">
  <h1 style="color:#1a1a1a;border-bottom:3px solid #0066cc;padding-bottom:10px">
    📰 Omni News 日报
  </h1>
  <div style="background:#f0f7ff;padding:15px;border-radius:8px;margin:15px 0">
    <strong>📌 今日一句话:</strong> ...
  </div>
  <!-- 每个板块 -->
  <h2 style="color:#0066cc">🤖 AI 人工智能</h2>
  <!-- 每条新闻卡片 -->
  <div style="border-left:4px solid #0066cc;padding-left:15px;margin:10px 0">
    <strong>标题</strong>
    <p style="color:#666">摘要</p>
    <small style="color:#999">来源 | 时间</small>
  </div>
</div>
```

#### 4C: 图片（社交媒体分享，from TrendSonar）

- 生成热点新闻卡片图片
- 使用 Pillow 生成
- 适合分享到社交媒体

#### 4D: PDF（归档场景）

- 使用 LaTeX/WeasyPrint 生成
- 适合打印或离线阅读
- 包含完整目录和图表

#### 4E: RSS（订阅场景）

```xml
<!-- 日报 RSS feed -->
<rss version="2.0">
  <channel>
    <title>Omni News Daily</title>
    <item>
      <title>新闻标题</title>
      <description>摘要</description>
      <pubDate>...</pubDate>
    </item>
  </channel>
</rss>
```

### 5. 报告生成策略（from TrendSonar）

#### 5A: 日报/周报/月报

| 频率 | 内容 | 缓存策略 |
|------|------|---------|
| 日报 | 当天热点+情感+趋势 | 当天有效，次日重新生成 |
| 周报 | 7天趋势+专题回顾+下周展望 | 生成后缓存7天 |
| 月报 | 30天趋势+月度热点+情感演变 | 生成后缓存30天 |

#### 5B: 报告可视化元素

| 图表类型 | 用途 | 来源 |
|---------|------|------|
| 来源分布饼图 | 展示各源占比 | TrendSonar |
| 词云 | 高频关键词 | TrendSonar |
| 情感分布 | 正/中/负占比 | TrendSonar |
| 热度趋势折线图 | 热度随时间变化 | TrendSonar |
| 词项共现网络 | 关键词关联 | TrendSonar |
| 专题时间轴 | 事件演变 | TrendSonar |

#### 5C: AI 报告 Prompt 模板（from TrendSonar）

```yaml
# 流式输出报告（边生成边展示）
REPORT_PROMPT: |
  你是一位资深新闻分析师。基于以下新闻数据，生成一份{period}度分析报告。
  
  报告结构:
  1. 一句话总结
  2. 核心发现（3-5个要点）
  3. 热点事件回顾（含时间轴）
  4. 情感分析（正/中/负分布）
  5. 关键词网络
  6. 风险与机会
  7. 后续观察要点
  
  要求:
  - 使用 Markdown 格式
  - 每个要点附带具体数据
  - 情感分析用 emoji 标注
  - 重要数字加粗
  - 每个板块之间用分隔线

# 情感分析路由
AI_ROUTE:
  SUMMARY: "main"        # 摘要用主力模型
  SENTIMENT: "backup"    # 情感分析用备用模型（省成本）
  CLUSTERING: "backup"   # 聚类用备用模型
  REPORT: "main"         # 报告用主力模型
```

### 6. Deep Fetch 深度穿透（from cclank）

#### 6A: 适用场景

- 新闻标题含关键数据但正文才有详情
- 需要提取完整事件背景
- 需要多篇文章交叉验证

#### 6B: 实现方式

```python
# 使用 Playwright 绕过 Cloudflare 等反爬
from playwright.sync_api import sync_playwright

def deep_fetch(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        content = page.content()
        # 提取正文（使用 readability 算法）
        article = extract_article(content)
        browser.close()
        return article

# 将完整正文交给 LLM 做摘要和过滤
llm_summary = llm.summarize(article.text, max_length=200)
```

#### 6C: 防降智过滤（from cclank）

- LLM 阅读完整正文后判断:
  - 是否与用户关注的话题相关
  - 信息密度是否足够（排除水文）
  - 是否有独立观点（排除洗稿）
  - 时效性是否满足要求

### 7. 多模型路由策略（from TrendSonar）

#### 7A: 模型分工

| 任务 | 模型 | 原因 |
|------|------|------|
| 新闻摘要 | 主力模型（Claude/GPT） | 需要高质量总结 |
| 情感分析 | 备用模型（DeepSeek） | 简单任务，省成本 |
| 去重判断 | 备用模型 | 简单的是/否判断 |
| 聚类验证 | 备用模型 | 需要速度优先 |
| 报告生成 | 主力模型 | 需要深度分析 |
| 专题命名 | 备用模型 | 简单任务 |
| 对话回复 | 主力模型 | 需要理解上下文 |

#### 7B: 故障转移

```
主力模型失败 → 自动切换备用模型 → 仍失败 → 降级为纯文本输出
```

### 8. 信源健康监控（from TrendSonar）

#### 8A: 健康指标

| 指标 | 阈值 | 动作 |
|------|------|------|
| 最近抓取成功率 | < 80% | 标记为降级 |
| 连续失败次数 | > 3 | 暂停该源，通知管理员 |
| 平均响应时间 | > 10s | 降低抓取频率 |
| 内容质量评分 | < 5/10 | 降低权重或暂停 |

#### 8B: 数据清理

- 自动清理低热度历史数据（默认保留30天）
- 高热度事件永久保留
- 每日凌晨执行清理任务

---

## 存档

```
memory/daily_news_YYYY-MM-DD.md                    — 完整日报
memory/daily_news_YYYY-MM-DD-brief.md              — 快速简报
memory/daily_news_YYYY-MM-DD-sentiment.md          — 舆情分析
memory/daily_news_YYYY-MM-DD-events.json           — 事件聚类数据（结构化）
memory/daily_news_YYYY-MM-DD-report.html           — HTML 格式报告
memory/daily_news_YYYY-MM-DD-topics.md             — 专题追踪数据
memory/daily_news_YYYY-MM-weekly.md               — 周报
memory/daily_news_YYYY-MM-monthly.md               — 月报
```

## Cron 建议

| 班次 | 时间 | 内容 |
|------|------|------|
| 早报 | 08:30 | 前一日汇总 + 国际夜间动态 |
| 午报 | 12:00 | 上午快讯 |
| 晚报 | 20:30 | 全量日报（联播上线后） |
| 舆情 | 10:00/16:00 | 情感分析 + 趋势预警 |

## 方法论提取（从 GitHub 项目学习）

### 来自 AI News Digest
- **5 道 QA Gate**: 数据源健康检查→去重交叉验证→信号分级→事实核验→完整性自检
- **9 层信源系统**: 中文核心→英文一手→数据型→Builder→趋势研究→微信生态→MCP→AI HOT
- **信号分级**: 重磅 / 值得关注 / 常规
- **断点续跑**: 用 `.progress` / `.done` 标记阶段状态

### 来自 TrendSonar — ⭐NEW v3.1 核心方法论
- **多阶段去重流水线**: URL精确去重→Embedding语义去重(阈值0.85)→AI核验→事件聚类
- **MinHash LSH + HDBSCAN**: 近似最近邻搜索+密度聚类，自动发现事件簇
- **专题自动发现**: 从高热新闻中发现候选事件簇→AI审核生成专题→时间轴+趋势仪表盘
- **多模型路由**: 按任务复杂度分配主力/备用模型，摘要和报告用主力，情感/聚类用备用
- **流式报告生成**: 边生成边输出，关键词深度报告含事件演变+观点光谱+风险机会+后续观察
- **智能体问答**: 基于PydanticAI构建新闻智能体，支持连续对话+工具调用
- **信源健康监控**: 抓取成功率/响应时间/内容质量三维评分，自动降级低质量源
- **数据生命周期**: 低热度自动清理(默认30天)，高热度永久保留
- **Deep正文抓取**: Crawl4AI+Playwright补抓正文，支持动态页面等待+超时+重试+并发控制

### 来自 cclank/news-aggregator-skill — ⭐NEW v3.1 输出方法论
- **杂志级排版**: 视觉层次清晰+信息密度适中+emoji视觉锚点+来源标注+可信度分级
- **场景化早报**: 财经早报/科技早报/吃瓜早报/AI深度日报 四套模板
- **OPML自定义订阅**: 兼容Feedly/Inoreader导出，任意RSS源即插即用
- **Deep Fetch穿透**: Playwright绕过Cloudflare反爬，LLM过滤提炼完整正文
- **防降智过滤**: LLM判断相关性+信息密度+独立观点+时效性，排除水文和洗稿
- **44+高价值信源**: 精选跨硅谷/中国创投/开源/金融/国际/AI播客的顶级渠道

### 来自 chronicle — ⭐NEW v3.1 聚类方法论
- **语义Embedding**: 使用SentenceTransformer/paraphrase-multilingual-MiniLM-L12-v2生成向量
- **MinHash LSH**: 局部敏感哈希做近似最近邻搜索，O(n)复杂度
- **HDBSCAN聚类**: 基于密度的层次聚类，自动确定簇数量，无需预设K值
- **时间线生成**: 将同一事件的多源报道按时间排列，生成连贯的事件时间线

### 来自 Follow Builders
- **Follow builders, not influencers**: 追踪真正做产品的人，不是信息搬运工
- **中央 Feed 模式**: 所有源集中抓取，agent 只请求一次 JSON
- **Remix 摘要**: 原始内容 → 个性化摘要 → 投递到消息渠道

### 来自 BettaFish（微舆）
- **多Agent协作**: Query/Media/Insight/Report 四类 Agent 各司其职
- **论坛辩论机制**: Agent 间链式思维碰撞，避免单一模型局限
- **微调情感模型**: BERT/GPT-2 LoRA 针对微博情感微调
- **公私域融合**: 公开舆情 + 内部数据库联合分析

### 来自 60s API
- **零Key设计**: 所有接口无需注册，降低接入门槛
- **CDN加速**: 全球CDN确保毫秒级响应
- **多运行时**: Deno/Bun/Node.js/Cloudflare Workers 灵活部署

### 来自 DailyHotApi
- **40+平台聚合**: 一个 API 覆盖几乎所有中文互联网热榜
- **JSON+RSS双模式**: 同时支持 API 调用和 RSS 订阅
- **60分钟缓存**: 避免频繁请求官方数据

### 来自 NewsMCP
- **事件聚类**: 用向量嵌入将同一事件的多源报道自动分组
- **影响评分**: 基于 source_count + impact_score 排序
- **12 话题 × 30 地区** 矩阵覆盖

### 来自 parkervg/news-article-clustering
- **实体增强TF-IDF**: 非人名实体权重×4，人名×1.3
- **多聚类算法对比**: K-Means / HAC / BIRCH 三种算法对比效果
- **可视化**: Seaborn + Matplotlib + D3 多维度展示

---

## 新发现项目记录（v3.0-v3.1 研究）

### 直接可用（已集成）
| 项目 | Stars | 用途 | 集成方式 |
|------|-------|------|---------|
| vikiboss/60s | 5.8k | 实时热搜全平台 | API 直接调用 |
| imsyy/DailyHotApi | 4.1k | 40+平台聚合 | API 直接调用 |

> ~~TrendRadar~~ 已移除（监控+推送功能超出新闻日报核心定位）

### 核心方法论提取（未安装，已提取方法论）
| 项目 | Stars | 用途 | 提取内容 |
|------|-------|------|---------|
| 666ghj/BettaFish | 42.2k | 多Agent舆情 | 协作机制+情感模型 |
| aicezam/trendsonar | - | 新闻聚合Web平台 | 去重流水线+多模型路由+专题追踪+流式报告+信源监控 |
| cclank/news-aggregator-skill | - | 44+信源Agent技能 | 杂志级排版+场景化早报+Deep Fetch+OPML+防降智 |
| dukeblue1994-glitch/chronicle | - | 事件检测+时间线 | MinHash LSH + HDBSCAN + Embedding |
| parkervg/news-article-clustering | - | 新闻聚类 | 实体增强TF-IDF+多算法对比 |
| wangy8989/Chinese-Financial-News-Sentiment-Analysis | 17 | 金融情感 | BERT微调方法 |
| ksv-muralidhar/find_similar_news | - | 相似新闻过滤 | SentenceTransformer+PCA+余弦相似度 |
| AdirthaBorgohain/reportAI | - | LLM生成PDF报告 | 报告模板+去重+自动图表 |
| jhangyu/palimpsest | 0 | AI RSS生成 | 全文本RSS生成方法 |

### 已排除（不兼容/过重）
| 项目 | 原因 |
|------|------|
| BettaFish 直接部署 | 需 PostgreSQL + LLM API + Docker，过重 |
| thu-unicorn/NLP-Chinese-Sentiment-Analysis | 学术项目，0 stars，不活跃 |
| tophub-api | 官方 API 收费，免费列表功能有限 |

---

## 付费源（已排除但记录）

| 源 | 费用 | 替代方案 |
|----|------|---------|
| tianapi-ai-news | 天聚数行 API Key | web_search + 36氪 |
| google-news-api (Scavio) | 50次免费后 $25/2500次 | web_search + NewsMCP + The Hear |
| jisu-news | 聚数付费 API | web_search |
| ifind-finance-data | iFind 付费 | WallstreetCN + Yahoo Finance |
| caixin-news | 财新付费墙 | web_search 间接覆盖 |
| X 官方 API | $200/月起 | twikit + web_search |
| tophubdata 详细内容 | 1u/快照 | 60s API + DailyHotApi |

---

## 免责声明

本技能生成的分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。

---

## 版本历史

- **v1.0.1** (2026-09-17): 
  - 安全修复：收窄触发词（移除"最新"、"热点"、"热搜"、"builder"等宽泛词汇）
  - 安全修复：Docker镜像固定版本（60s API v2.1.0, DailyHotApi v2.1.0）
  - 安全修复：移除非核心功能（天气/翻译/IP查询/QR码等实用端点）
  - 安全修复：移除TrendRadar监控推送引擎（功能越界风险）
  - 隐私增强：添加数据与隐私声明（第三方服务清单+用户控制说明）
  - 透明度：添加数据保留策略（日报30天/高热度永久/搜索不保留）
  - 误报修复：HTML模板注释格式调整，避免提示注入误判

- **v1.0.0** (2026-09-17): 
  - 初始发布：9引擎新闻聚合 + 情感分析 + 自动进化系统
  - 82个免费源覆盖（23社媒+15国内+21国际+15 Builder+8工具）

- ~~v3.1~~ (内部版本): 
  - 新增信息反馈优化模块（8大优化维度）
  - 新增去重与事件聚类流水线
  - 新增场景化早报模式（8套模板）
  - 新增杂志级排版原则
  - 新增多格式输出（Markdown/HTML/图片/PDF/RSS）
  - 新增Deep Fetch深度穿透
  - 新增个性化关键词追踪与智能推送
  - 新增多模型路由策略（按任务复杂度分配主/备模型）
  - ⭐ 新增信源健康监控（成功率/响应时间/内容质量三维评分）
  - ⭐ 新增事件聚合展示模板（多源对比+情感分布+趋势）
  - 来自 TrendSonar 方法论: 多阶段去重+专题追踪+流式报告+智能体问答
  - 来自 cclank 方法论: 杂志排版+场景化模板+OPML订阅+Deep Fetch
  - 来自 chronicle 方法论: MinHash LSH + HDBSCAN + 时间线生成
  - 来自 reportAI 方法论: LLM驱动PDF报告生成
- **v3.0** (2026-09-17): 
  - ⭐ 新增引擎8 (60s API): 微博/知乎/抖音/小红书/B站/头条/百度/猫眼/豆瓣/IT之家/贴吧/懂车帝/快手
  - ⭐ 新增引擎9 (DailyHotApi): 40+平台包括快手/贴吧/虎扑/V2EX/地震速报/气象预警
  - ⭐ 新增情感分析层: SnowNLP/PaddleNLP/BettaFish方法论
  - 社交媒体从 4 平台扩展到 **18 平台全覆盖**
  - 免费源从 50+ 扩展到 **80+**
  - 新增舆情分析模式输出
- **v2.0** (2026-09-17): 整合 GitHub 发现（NewsMCP, Follow Builders, InBrief, AI News Digest, twikit, ALL-about-RSS），新增 AI Builder 动态引擎，免费源从 35 扩展到 50+
- **v1.0** (2026-09-17): 初始版本，35 个免费源，5 层引擎
