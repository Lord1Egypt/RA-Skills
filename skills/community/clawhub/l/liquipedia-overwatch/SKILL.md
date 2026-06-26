---
name: liquipedia-overwatch
description: ow数据查询技能。当用户询问 Liquipedia Overwatch 数据时激活。
---

# Liquipedia Overwatch 数据查询技能

---

# 第一部分：本地缓存系统

所有成功抓取的数据都应保存至本地缓存，下次查询时优先读缓存。

## 缓存目录结构

```
/workspace/liquipedia-cache/
├── index.json                          # 主索引
├── tournaments/                        # 赛事数据（按 schema.md tournaments/ 格式）
├── teams/                              # 战队数据（按 schema.md teams/ 格式）
├── players/                            # 选手数据（按 schema.md players/ 格式）
├── hero_picks/                         # 英雄选取数据
├── matches/                            # 比赛结果（按 schema.md matches/ 格式）
└── earnings/                           # 奖金排名
```

## 缓存管理命令

```bash
# 查看所有缓存
python3 references/cache_manager.py list

# 查看某类型缓存
python3 references/cache_manager.py list team

# 读取已缓存的数据（JSON）
python3 references/cache_manager.py load team weibo-gaming
python3 references/cache_manager.py load tournament owcs-2026-china-s1
python3 references/cache_manager.py load match owcs-2026-china-s1-swiss-r1

# 按关键词搜索缓存内容
python3 references/cache_manager.py query Guxue

# 保存结构化数据到缓存（自动写 index.json）
python3 references/cache_manager.py save team weibo-gaming '<json_string>'
python3 references/cache_manager.py save tournament owcs-2026-china-s1 '<json_string>'

# 重建索引
python3 references/cache_manager.py update-index
```

## 查询标准流程

```
Step 1 — 查本地缓存
  exec: python3 references/cache_manager.py load <type> <id>
  → 有数据且在有效期内？
      读取结构化 JSON → 转换为人类可读格式 → 直接返回
      （无需重新抓取）

Step 2 — 用 Playwright Scraper 抓取 Liquipedia（未命中或过时）
  exec: node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js "<URL>"
  → 等待页面加载（5-15秒），输出 JSON（含 contentPreview 文本和 screenshot 路径）
  → 从 contentPreview 中提取数据，严格按 schema.md 字段名填入 JSON

Step 3 — 按 schema.md 格式保存至缓存
  exec: python3 references/cache_manager.py save <type> <id> '<json>'
  → 必须包含根字段：schema_version、source_url、last_updated

Step 4 — 整合并输出
  缓存结构化 JSON → 第七部分人类可读模板 → 注明数据来源 URL 和时间
```

**数据有效期：**
- 赛程/赛果数据：赛事期间当天重新抓取
- 阵容/转会数据：本周内有效
- 历史战绩/奖金数据：可长期缓存

**⚠️ 重要：Liquipedia 对 direct HTTP 请求返回 403，必须始终用 Playwright Scraper 脚本抓取。**
**⚠️ 所有写入缓存的 JSON 必须严格遵循 schema.md 的字段名和嵌套结构（见下方各类型提取规范）。**

---

# 第二部分：数据源概述

Liquipedia 是守望先锋电竞最权威的维基数据源，涵盖：

| 数据类型 | 内容 |
|---|---|
| 赛事 | OWCS / OWL / OWWC / 大学生赛 / B-Tier 等各级别 |
| 赛区 | NA / EMEA / 亚太(含韩国/日本/中国) / 中国 |
| 选手 | 职业选手页面，含战队、位置、成就、奖金 |
| 战队 | 战队主页，含历史、阵容、战绩、奖金 |
| 统计 | 选手收入排名、战队奖金排名、各类排行榜 |
| 转会 | 选手转会历史记录 |

**OWTV.gg（辅助数据源）：**
OWTV.gg 是 OWCS 官方合作平台，提供 Liquipedia 没有的详细英雄选取数据，是本技能的辅助数据源。

| 数据类型 | 覆盖范围 | 说明 |
|---|---|---|
| 英雄选取 | OWCS 全赛区 | ⚠️ **独特优势**，含 per-map per-team per-hero 详细数据；无 recap 时抓 /matches/{id} 含逐场统计 |
| 选手数据 | OWCS 全赛区 | /matches/{id} 含每位选手伤害量/治疗量/抵挡伤害等详细面板数据 |
| 赛程/赛果 | OWCS 全赛区 | /matches 实时赛程和最新赛果；/matches/{id} 含单场详细英雄数据 |
| 阵容公告 | OWCS 全赛区 | /news 含各队阵容公告和转会动态 |
| 赛事报道 | OWCS 全赛区 | 战报含详细比分、地图、选手表现 |

**与 Liquipedia 的分工：**
- **Liquipedia 优先**：英雄选取数据（hero_picks）
- **OWTV.gg 优先**：实时赛程（`/matches`）+ 逐场英雄数据（`/matches/{id}`）
- **Liquipedia 优先**：阵容公告与转会（teams/roster news）
- **Liquipedia 优先**：选手档案、战队历史、奖金数据
- **OWTV.gg 补充**：Liquipedia 缺失的选手近况、阵容变动

---

# 第三部分：核心 URL 模式

```
# 赛区主页
https://liquipedia.net/overwatch/Overwatch_Champions_Series
https://liquipedia.net/overwatch/Overwatch_League
https://liquipedia.net/overwatch/Overwatch_World_Cup

# OWCS 赛事页面（按赛区+年份+阶段）
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/NA/Stage_1
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/EMEA/Stage_1
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/Korea/Stage_1
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/Asia/Stage_1/Pacific

# OWCS 全阶段
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/Midseason_Championship
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/Champions_Clash
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/World_Finals

# OWWC
https://liquipedia.net/overwatch/Overwatch_World_Cup/2026
https://liquipedia.net/overwatch/Overwatch_World_Cup/2026/Conference_Cups

# OWL
https://liquipedia.net/overwatch/Overwatch_League/2026/Season_1

# 选手与战队
https://liquipedia.net/overwatch/{PlayerName}    # 例: https://liquipedia.net/overwatch/Guxue
https://liquipedia.net/overwatch/{TeamName}     # 例: https://liquipedia.net/overwatch/Weibo_Gaming

# 统计门户
https://liquipedia.net/overwatch/Portal:Statistics
https://liquipedia.net/overwatch/Portal:Statistics/Player_earnings
https://liquipedia.net/overwatch/Portal:Statistics/Team_earnings

# 选手转会
https://liquipedia.net/overwatch/Player_Transfers

# 赛事列表
https://liquipedia.net/overwatch/B-Tier_Tournaments/2026
```

**team-id 规范（小写、横线）：**
```
weibo-gaming   → 微博电竞
jdg             → JDG
all-gamers      → All Gamers
solus-victorem  → Solus Victorem
naive-piggy     → Naive Piggy
homie-e         → Homie E
deg             → DEG
milk-tea        → Milk Tea
dongdong        → DongDong
```

---

## OWTV.gg URL 模式

```
# 主页与导航
https://owtv.gg                          # 主页
https://owtv.gg/matches                  # 赛程与赛果（实时）
https://owtv.gg/news                      # 新闻文章列表
https://owtv.gg/fantasy                  # Fantasy 页面

# 新闻文章（slug 格式）
https://owtv.gg/news/grand-finals-recap-owcs-pre-season-bootcamp   # 战报（英雄选取）
https://owtv.gg/news/all-gamers-reveal-2026-roster                 # 阵容公告
https://owtv.gg/news/milk-tea-announce-new-roster-for-2026         # 阵容公告
https://owtv.gg/news/owcs-2026-stage-1-korea-preview               # 赛事预览
https://owtv.gg/news/owcs-2026-stage-1-emea-preview                # 赛事预览
https://owtv.gg/news/owcs-2026-stage-1-china-preview               # ⚠️ 注意：部分 slug 可能为 404
```

**OWTV.gg slug 规范（小写、横线）：**
```
格式: {team-or-event-name}-announce-{year}-roster
格式: {tournament}-{region}-{stage}-{preview/recap}
示例: milk-tea-announce-new-roster-for-2026
示例: owcs-2026-stage-1-korea-preview
示例: grand-finals-recap-owcs-pre-season-bootcamp
```

---

## Liquipedia 页面层级架构（完整参考）

### 📐 整体层级树（6 层）

```
Level 0 — 入口层
│
├── Level 1 — 赛事体系主页（按赛事类型）
│   ├── /Overwatch_Champions_Series       ← OWCS 总览（2024至今）
│   ├── /Overwatch_League                ← OWL 总览（历史，2018-2023）
│   ├── /Overwatch_World_Cup             ← OWWC 总览（每年）
│   ├── /Overwatch_Contenders            ← OC（历史）
│   └── /B-Tier_Tournaments/{年份}       ← B-Tier 赛事索引
│
├── Level 2 — 具体赛事页（按年份/赛区/阶段）⭐最高价值层
│   ├── OWCS 2026 China/NA/EMEA/Korea/Asia S1
│   ├── OWCS 2026 Midseason Championship
│   ├── OWCS 2026 World Finals
│   ├── OWL {年份}/Season {X}/Regular_Season
│   └── OWWC {年份} / Conference_Cups
│
├── Level 3 — 战队 / 选手主页
│   ├── /Weibo_Gaming
│   ├── /Guxue
│   └── /{PlayerName}
│
├── Level 4 — 统计与数据库
│   └── /Portal:Statistics
│       ├── /Player_earnings              ← 全球选手奖金排行
│       ├── /Player_earnings/China       ← 中国选手奖金排行
│       ├── /Team_earnings               ← 战队奖金排行
│       └── /Statistics/{年份}/...         ← 年度统计
│
└── Level 5 — 功能与工具页
    ├── /Match_List                      ← 所有赛果索引
    ├── /Player_Transfers               ← 转会记录
    ├── /Category:Teams                 ← 战队分类列表
    ├── /Category:Players               ← 选手分类列表
    └── /api.php                        ← 搜索 API（可用 extract_content）
```

---

### 🔷 Level 1 — 赛事体系主页

#### `/Overwatch_Champions_Series` — OWCS 总览
OWCS（Overwatch Champions Series）顶层入口，2024 年推出，取代原 OWL 地位。

**能提供的信息：**
- 所有赛区（China / NA / EMEA / Korea / Asia Pacific）当前赛季概览
- OWCS 赛季整体结构（Stage 1 → Midseason → Stage 2 → World Finals）
- 奖金池总量和赛季总积分体系
- 当前赛季 Partner Teams 名单（按赛区）

```
https://liquipedia.net/overwatch/Overwatch_Champions_Series
```

#### `/Overwatch_League` — OWL 总览
历史赛季汇总（2018–2023）。

**能提供的信息：**
- 各赛季历史排名入口、Franchise 战队列表
- OWL 已于 2024 年停办，被 OWCS 取代（S-Tier 赛事并入 OWCS）

```
https://liquipedia.net/overwatch/Overwatch_League
```

#### `/Overwatch_World_Cup` — OWWC 总览
世界杯体系主页。

**能提供的信息：**
- 各届 OWWC 赛果（2023 / 2024 / 2026 …）
- Conference Cups（洲际杯）入口
- 2026 赛季预计 30 支队伍（19 支受邀 + 11 支外卡）

```
https://liquipedia.net/overwatch/Overwatch_World_Cup
```

#### `/B-Tier_Tournaments/{年份}` — B-Tier 赛事索引
非顶级赛事（大学生赛、社区赛等）。

**能提供的信息：**
- 按年份列出所有 B-Tier 赛事
- 每项赛事含参赛队伍、赛果

```
https://liquipedia.net/overwatch/B-Tier_Tournaments/2026
```

---

### 🔷 Level 2 — 具体赛事页（⭐最高价值层）

> **这是所有赛程、比分、阵容的核心数据层。**
> **一网打尽**：一个赛事主页含阵容 + 赛程 + 赛果，优先抓取此层。

#### OWCS 赛事 URL 模式

```
/Overwatch_Champions_Series/{年份}/{赛区}/{阶段}
/Overwatch_Champions_Series/{年份}/{赛事名称}
```

| 页面 | URL 示例 |
|---|---|
| OWCS 2026 中国 S1 | `/2026/China/Stage_1` |
| OWCS 2026 NA S1 | `/2026/NA/Stage_1` |
| OWCS 2026 EMEA S1 | `/2026/EMEA/Stage_1` |
| OWCS 2026 Korea S1 | `/2026/Korea/Stage_1` |
| OWCS 2026 亚太 S1 | `/2026/Asia/Stage_1/Pacific` |
| OWCS 2026 季中杯 | `/2026/Midseason_Championship` |
| OWCS 2026 世界总决赛 | `/2026/World_Finals` |
| OWCS 2026 冠军杯 | `/2026/Champions_Clash` |
| OWCS 2026 季前训练营 | `/2026/Stage_1/Pre-Season_Bootcamp` |

**能提供的信息（全部来自一个页面）：**
- 赛事基本信息（日期、奖金池、赛制）
- 所有参赛战队名单 + 种子序号（`teams[]`）
- 瑞士轮（Swiss）/ 循环赛（Round Robin）赛程与赛果
- 淘汰赛（Playoffs）赛程与赛果
- **各队完整阵容**（直接抓取，无需单独访问战队主页）
- MVP / 最佳阵容（部分赛事）

#### OWL 赛事 URL 模式

```
/Overwatch_League/{年份}/Season_{X}
/Overwatch_League/{年份}/Season_{X}/Regular_Season
/Overwatch_League/{年份}/Season_{X}/Playoffs
```

| 页面 | URL 示例 |
|---|---|
| OWL {年份} 主页面 | `/Overwatch_League/2026/Season_1` |
| OWL {年份} 常规赛 | `/Overwatch_League/2026/Season_1/Regular_Season` |
| OWL {年份} 季后赛 | `/Overwatch_League/2026/Season_1/Playoffs` |

> ⚠️ OWL 已整合入 OWCS 为 S-Tier 赛事，但仍保留独立页面

#### OWWC 赛事 URL 模式

```
/Overwatch_World_Cup/{年份}
/Overwatch_World_Cup/{年份}/Conference_Cups
```

| 页面 | URL 示例 |
|---|---|
| OWWC {年份} 总览 | `/Overwatch_World_Cup/2026` |
| OWWC {年份} 洲际杯 | `/Overwatch_World_Cup/2026/Conference_Cups` |

**能提供的信息：**
- 赛程（小组赛 Round Robin → 瑞士轮 Swiss → 淘汰赛）
- 各国家队阵容（国家队非俱乐部）
- 最终排名

---

### 🔷 Level 3 — 战队 / 选手主页

#### 战队页 `/Overwatch/{TeamName}`（斜杠分隔，空格变下划线）

```
/Weibo_Gaming
/Falcons           # Team Falcons（斜杠前缀省略）
/New_Era
/Milk_Tea
```

**能提供的信息（Infobox 重点区域）：**
- 战队成立年份、所属地区（Region）
- 当前赛季完整阵容（Tank / DPS / Support 分组，player_id 必填）
- 教练组（coaches[]）
- 历届赛季成绩（History）
- 荣誉墙（冠军 / 亚军 / 季军次数）
- ⚠️ 中文战队名不在 URL slug 中，Infobox 侧边栏才有中文名

**抓取优先级：** 赛事主页（Level 2）已含阵容时，优先从赛事主页批量获取；战队主页用于补充历史阵容和荣誉。

#### 选手页 `/Overwatch/{PlayerName}`（空格分隔，空格变下划线）

```
/Guxue
/LIP
/Viol2t
/ChiYo_
```

**能提供的信息（Infobox 重点区域）：**
- 真名、国籍、出生日期
- 当前战队（current_team）、位置（Tank / DPS / Support）
- 生涯荣誉（Achievements）
- 累计奖金（Total Earnings）
- 擅长英雄（Heroes）
- 战队历史（Teams History，含 from/to 日期）
- ⚠️ 这是唯一能获取选手真实姓名的页面

---

### 🔷 Level 4 — 统计数据库

#### `/Portal:Statistics` — 统计门户（综合入口）

```
https://liquipedia.net/overwatch/Portal:Statistics
```

**子页面（均为可抓取页面）：**

| URL | 内容 |
|---|---|
| `/Portal:Statistics/Player_earnings` | 全球选手奖金总排行 |
| `/Portal:Statistics/Player_earnings/China` | 中国选手奖金排行 |
| `/Portal:Statistics/Player_earnings/Korea` | 韩国选手奖金排行 |
| `/Portal:Statistics/Team_earnings` | 战队奖金总排行 |
| `/Portal:Statistics/{年份}/Organization_Winnings` | {年份}年度战队奖金 |
| `/Portal:Statistics/{年份}/Player_Winnings` | {年份}年度选手奖金 |

**能提供的信息：**
- 按奖金总额排序的选手/战队排名（跨所有赛事）
- 历届年份筛选（2015–2026）
- 地区筛选（China / Korea / NA / EMEA）
- 选手成就列表（Achievements 列）
- ⚠️ 奖金数据为累计值，含 OWL/OC/OWCS/OWWC 所有赛事

---

### 🔷 Level 5 — 功能与工具页

#### `/Match_List` — 赛果索引
按时间倒序列出所有已结束的比赛，**按月分组**。

```
/Match_List
/Match_List/2026
/Match_List/2026/March
```

**能提供的信息：**
- 所有赛事的历史赛果（跨赛事类型）
- 比分、地图胜局、日期
- **适用场景：** 查询某场历史比赛结果（已知大致日期时）

#### `/Player_Transfers` — 转会记录
按时间倒序列出所有选手转会。

**能提供的信息：**
- 转会日期、原战队 → 新战队
- 转会类型（transfer / signing / loan / retirement）
- ⚠️ 这是批量获取阵容变动的最高效入口，一次抓取全量转会信息

**适用场景：** 赛季初批量更新所有战队阵容变动

#### `/api.php` — 搜索 API（可用 extract_content）
无需 Playwright 的 API 端点（可用 extract_content_from_websites 直接访问）。

```
/api.php?action=opensearch&search={关键词}
  → 返回关键词匹配的页面标题列表（可用于自动发现 slug）

/api.php?action=query&list=search&srsearch={关键词}
  → 返回页面标题 + URL + 摘要片段
```

**适用场景：**
- 不知道战队/选手页面的准确 slug 时
- 搜索 "Milk Tea" → 返回 `/Milk_Tea`
- 搜索 "Guxue team" → 返回 `/Guxue`

---

### 📊 页面数据覆盖矩阵（抓取优先级参考）

| 数据类型 | 最佳页面 | 工具 | 价值 |
|---|---|---|---|
| 实时赛程与赛果 | Level 2 赛事页 | Playwright stealth | ⭐⭐⭐⭐⭐ |
| 战队当前阵容 | Level 2 赛事页（批量） | Playwright stealth | ⭐⭐⭐⭐⭐ |
| 选手详细档案 | Level 3 选手页 | Playwright stealth | ⭐⭐⭐⭐ |
| 战队历史荣誉 | Level 3 战队页 | Playwright stealth | ⭐⭐⭐ |
| 选手累计奖金 | Level 4 统计门户 | Playwright stealth | ⭐⭐⭐ |
| 战队奖金排行 | Level 4 统计门户 | Playwright stealth | ⭐⭐⭐ |
| 批量转会动态 | Level 5 转会页 | Playwright stealth | ⭐⭐⭐ |
| 赛事积分体系 | Level 1 OWCS 总览 | Playwright stealth | ⭐⭐ |
| 历史赛果追溯 | Level 5 赛果索引 | Playwright stealth | ⭐⭐ |
| slug 自动发现 | Level 5 API | extract_content | ⭐⭐ |
| **英雄选取数据** | **❌ Liquipedia 无此数据** | **必须用 OWTV.gg** | — |

---

### 🔍 Playwright 抓取优先级推荐

按以下顺序依次抓取：

```
🥇 Level 2 赛事页
   → 一页搞定：阵容 + 赛程 + 赛果 + 赛制
   → 每赛季优先抓此层，再补充战队/选手详情

🥈 Level 3 选手/战队页
   → 选手真实姓名、国籍、战队历史
   → 战队荣誉墙、历史战绩

🥉 Level 4 统计门户
   → 奖金排名（当用户问"谁奖金最高"时）
   → 跨年份对比

4. Level 5 转会页
   → 赛季初批量抓取所有阵容变动

5. Level 1 赛事总览页
   → 赛季结构和积分体系（一次性知识）
```

> **⚠️ 硬性规则：** Liquipedia 对 direct HTTP 请求返回 403，**Level 1–5 所有页面均必须通过 Playwright Scraper 抓取**，唯 `/api.php` 可直接用 `extract_content_from_websites` 访问。

---

# 第四部分：赛事体系速查

## OWCS（Overwatch Champions Series）

| 赛区 | 赛事周期 | 说明 |
|---|---|---|
| Korea | 3月-5月 | OWCS 韩国赛区 |
| China | 3月-4月 | OWCS 中国赛区（8支队伍） |
| NA | 3月-4月 | OWCS 北美赛区 |
| EMEA | 3月-4月 | OWCS 欧洲/中东/非洲赛区 |
| Asia/Pacific | 3月-4月 | OWCS 亚太赛区（含日本） |
| Midseason Championship | 7月-8月 | OWCS 季中赛（利雅得，$1,000,000） |
| World Finals | 12月 | OWCS 全球总决赛 |
| Champions Clash | 5月 | OWCS 冠军杯 |

## OWWC（Overwatch World Cup）

- 2026年预计30支队伍参赛（19支受邀+11支外卡）
- Conference Cups 3-4月，世界杯决赛待定
- 赛制：Round Robin + Swiss

## OWL（Overwatch League）

- 2026赛季改为 S-Tier 融入 OWCS 体系
- 部分赛季仍有独立页面

## 大学生/Collegiate 赛事

- NACE Spring 2026
- Overwatch Collegiate Spring 2026 Open

---

# 第五部分：抓取方法（Playwright Scraper + schema.md 字段规范）

## ⚠️ 使用 Playwright Scraper Skill

Liquipedia 对 direct HTTP 请求返回 403，**必须使用 Playwright Scraper Skill** 抓取。

**Playwright 脚本位置：**
```
/userspace/skills/playwright-scraper-skill-1-2-0/scripts/
```

**选择脚本的原则：**

| 情况 | 脚本 | 速度 |
|---|---|---|
| 先试 simple（速度快） | `playwright-simple.js` | 3-5s |
| simple 失败（403/Cloudflare）→ 换 stealth | `playwright-stealth.js` | 5-15s |
| Liquipedia 推荐直接用 stealth | — | — |

> ⚠️ Liquipedia 有 Cloudflare 反爬保护，**优先使用 stealth**，simple 遇到 403 时立即换用 stealth。

### Playwright 抓取标准流程

```bash
# Step 1: 运行 Playwright stealth 脚本抓取页面
cd /userspace/skills/playwright-scraper-skill-1-2-0
node scripts/playwright-stealth.js "<URL>"
# → 输出 JSON（含 title, contentPreview, screenshot 路径）

# Step 2: 从 contentPreview 提取结构化数据（见下方各类型提取规范）
# 严格按 schema.md 字段名填入 JSON

# Step 3: 可选截图 OCR（snapshot 提取困难时）
# 使用 images_understand 对截图进行 OCR
```

**多 URL 并行抓取：**

```bash
# 并行运行多个脚本实例（每个 URL 一个进程）
node scripts/playwright-stealth.js "<URL1>" &
node scripts/playwright-stealth.js "<URL2>" &
node scripts/playwright-stealth.js "<URL3>" &
wait
```

> 注意：每次抓取会自动等待 5 秒（WAIT_TIME 可通过环境变量调整），stealth 模式检测到 Cloudflare 时额外等待 10 秒。

### 按页面类型的提取规范（严格对齐 schema.md）

---

#### 赛事主页（→ tournaments/{event-id}.json）

```
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1
```

```json
node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js "https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1"
```

**提取为以下 schema 格式：**
```json
{
  "schema_version": "1.0",
  "source": "liquipedia_net",
  "tournament_id": "owcs-2026-china-s1",
  "name_zh": "OWCS 2026 中国赛区 Stage 1",
  "name_en": "OWCS 2026 China Stage 1",
  "region": "China",
  "tier": "A",
  "date_start": "2026-03-21",
  "date_end": "2026-04-26",
  "prize_pool": "USD 100,000",
  "format": "Swiss Stage (Bo3) → Round Robin (Bo3) → Playoffs (Bo5)",
  "teams": [
    { "team_id": "weibo-gaming", "seed": 1 },
    { "team_id": "jdg", "seed": 2 }
  ],
  "current_stage": "Swiss Stage",
  "swiss_standings": {
    "round_1": [
      { "team_a": "weibo-gaming", "team_b": "naive-piggy", "result": "WBG 2-0 NP" }
    ]
  },
  "last_updated": "<ISO8601>",
  "source_url": "<当前页面URL>"
}
```

> **抓取命令（stealth，推荐）：**
> ```bash
> node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js \
>   "https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1"
> ```

**提取规则：**
- `tournament_id`：由区域-年份-阶段拼接，小写横线，如 `owcs-2026-china-s1`、`owcs-2026-korea-s1`
- `teams[]`：战队 ID 从 URL 或页面列表获取，`seed` 从赛程表获取
- `swiss_standings`：按实际轮次记录每场对阵和比分
- 赛事主页含多战队阵容时，也在此页面一并提取（无需分别访问战队主页）

---

#### 选手主页（→ players/{player-id}.json）

```
https://liquipedia.net/overwatch/Guxue
```

```json
node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js "https://liquipedia.net/overwatch/Guxue"
```

**提取为以下 schema 格式：**
```json
{
  "schema_version": "1.0",
  "player_id": "Guxue",
  "name_zh": "徐秋林",
  "nationality": "CN",
  "role": "Tank",
  "current_team": "weibo-gaming",
  "teams_history": [
    { "team_id": "weibo-gaming", "from": "2025-04-30", "to": null },
    { "team_id": "once-again", "from": "2021-01-01", "to": "2025-04-29" }
  ],
  "achievements": [
    { "event": "OWCS 2025 China Stage 1", "result": "Champion" }
  ],
  "earnings_total": "USD 50,000",
  "heroes_main": ["Winston", "Reinhardt", "Zarya"],
  "last_updated": "<ISO8601>",
  "source_url": "<当前页面URL>"
}
```

**提取规则：**
- `role`：枚举值 `Tank` / `DPS` / `Support`，严格匹配
- `current_team`：kebab-case team-id，不知道时填英文名后续修正
- `teams_history[].to = null`：表示仍在该队
- `achievements[]`：只填有据可查的冠军/MVP/最佳阵容

---

#### 战队主页（→ teams/{team-id}.json）

```
https://liquipedia.net/overwatch/Weibo_Gaming
https://liquipedia.net/overwatch/Milk_Tea
```

```json
node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js "https://liquipedia.net/overwatch/Weibo_Gaming"
```

**提取为以下 schema 格式：**
```json
{
  "schema_version": "1.0",
  "team_id": "weibo-gaming",
  "team_name_zh": "微博电竞",
  "team_name_en": "Weibo Gaming",
  "region": "China",
  "league": "OWCS 2026",
  "roster": {
    "tank": [
      { "player_id": "Guxue", "name_zh": "徐秋林", "nationality": "CN", "joined": "2025-04-30" }
    ],
    "dps": [
      { "player_id": "Leave", "name_zh": "黄昕", "nationality": "CN", "joined": "2021-01-01" }
    ],
    "support": [
      { "player_id": "LeeSooMin", "name_zh": "李秀敏", "nationality": "KR", "joined": "2026-01-01" }
    ]
  },
  "coaches": [
    { "coach_id": "Dongsu", "role": "Head Coach", "nationality": "KR" }
  ],
  "changes": {
    "new_players": [
      { "player_id": "SUNZO", "from": "Team CC" }
    ],
    "departed_players": [
      { "player_id": "Mew", "to": "Sister Team" }
    ]
  },
  "last_updated": "<ISO8601>",
  "source_url": "<当前页面URL>"
}
```

**提取规则：**
- `roster.tank[]`、`roster.dps[]`、`roster.support[]`：各自独立数组，player_id 必填，其余选填
- `nationality`：枚举 `CN` / `KR` / `JP` / `NA` / `EMEA` 等，勿用中文国名
- `joined`：若页面未注明日期则填入该赛季开始日期
- `changes`：`new_players` / `departed_players` 双向至少填一方
- OWCS 赛事主页含所有战队阵容时，优先从赛事主页批量提取（一次抓完）

---

#### 比赛结果（→ matches/{event-id}-{stage}-{round}.json）

```
https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1
```

```json
node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js "https://liquipedia.net/overwatch/Overwatch_Champions_Series/2026/China/Stage_1"
```

**提取为以下 schema 格式：**
```json
{
  "schema_version": "1.0",
  "event_id": "owcs-2026-china-s1",
  "stage": "Swiss Stage",
  "round": 1,
  "date": "2026-03-21",
  "matches": [
    {
      "id": "owcs-2026-china-s1-s1-r1-m1",
      "team_a": "weibo-gaming",
      "team_b": "naive-piggy",
      "score_a": 2,
      "score_b": 0,
      "maps": [
        { "map": "Busan", "winner": "weibo-gaming", "score_a": 2, "score_b": 0 }
      ],
      "result": "weibo-gaming Win"
    }
  ],
  "last_updated": "<ISO8601>",
  "source_url": "<当前页面URL>"
}
```

**提取规则：**
- `id` 格式：`{event_id}-{stage_abbr}-r{round}-m{num}`，如 `owcs-2026-china-s1-swiss-r1-m1`
- `stage`：`Swiss Stage` / `Round Robin` / `Playoffs`
- `team_a` / `team_b`：均为 kebab-case team-id
- `maps[].winner`：等于 `team_a` 或 `team_b`，非队伍名称

---

#### 选手转会页（→ players/transfers.json）

```
https://liquipedia.net/overwatch/Player_Transfers
```

```json
node /userspace/skills/playwright-scraper-skill-1-2-0/scripts/playwright-stealth.js ""https://liquipedia.net/overwatch/Player_Transfers")

```

**提取为以下格式（写入 players/transfers.json）：**
```json
{
  "schema_version": "1.0",
  "transfers": [
    {
      "player_id": "Guxue",
      "from_team": "once-again",
      "to_team": "weibo-gaming",
      "date": "2025-04-30",
      "type": "transfer",
      "source_url": "<当前页面URL>"
    }
  ],
  "last_updated": "<ISO8601>",
  "source_url": "<当前页面URL>"
}
```

**提取规则：**
- `type`：枚举 `transfer` / `signing` / `loan` / `retirement`，无则留空
- 日期无法确定时填入赛季年份1月1日（保守估计）
- 只记录有明确来源的转会，自由人声明单独标注

---

#### OWTV.gg 数据抓取完整工作流（含比赛发现 + 选手分析）

OWTV.gg 数据分两层：**赛事列表层**（含比赛 ID）和**比赛详情层**（含选手面板数据）。
OWTV 页面均支持 `extract_content_from_websites`（无需 Playwright）。

---

### ⚡ 优化 1：OWTV 赛事 ID 速查

OWTV 赛事 ID 已固化在 `references/owtv-tournament-ids.md`，无需搜索直接查表：

| 赛区 | OWTV URL | 赛事ID |
|---|---|---|
| China Stage 1 | `/tournaments/56` | **56** |
| NA Stage 1 | `/tournaments/55` | 55 |
| Korea Stage 1 | `/tournaments/58` | 58 |
| Pacific Stage 1 | `/tournaments/57` | 57 |

> 不知道 China Stage 1 的 ID？直接搜索：
> `web_fetch({"url": "https://duckduckgo.com/html/?q=site:owtv.gg/tournaments+China+Stage+1+OWCS+2026"})`

---

### ⚡ 优化 2：OWTV 比赛 ID 批量发现

OWTV 比赛 ID **连续递增**，同一赛区同日比赛 ID 相邻。
已知某场比赛 ID（如 1230）后，向相邻数字探测即可批量发现所有比赛：

```bash
# 扫描 OWTV 赛事 56（China Stage 1）下的比赛 ID
for ID in $(seq 1228 1240); do
  RESULT=$(curl -s "https://owtv.gg/matches/$ID" -o /dev/null -w "%{http_code}" --max-time 3)
  [ "$RESULT" = "200" ] && echo "✅  $ID"
done
```

> 赛事 ID → 首批比赛 ID 参考（2026-03-21 首日）：
> - China Stage 1（/tournaments/56）：Match 1230~1233

**批量发现工作流：**
```
1. 抓赛事页 → curl 探测相邻 ID → 找到所有已结束比赛的 match-id
2. 批量 extract_content 每场 /matches/{id} → 获取选手面板数据
3. 合并写入 hero_picks/{event-id}-day{n}.json
```

---

### ⚡ 优化 3：OWTV 比赛详情抓取（选手面板数据）

OWTV 每场比赛页含完整选手面板：**Elim / Ast / Dth / DMG / Heal / Mit**（6项数据）。

**OWTV 比赛详情页 URL 模式：**
```
https://owtv.gg/matches/{match-id}
```

**提取命令（无需 Playwright）：**
```json
extract_content_from_websites(tasks=[
  {
    "url": "https://owtv.gg/matches/1230",
    "prompt": "Extract ALL data for every player on every map: role, player ID, Eliminations, Assists, Deaths, Damage, Healing, Mitigation. Include map names, team names, final score."
  }
])
```

**hero_picks（含选手详细数据）提取格式：**
```json
{
  "schema_version": "2.0",
  "source": "owtv_gg",
  "team_id": "weibo-gaming",
  "event_id": "owcs-2026-china-s1",
  "match_id": "1233",
  "overall_stats": {
    "WBG": { "kills": 45, "deaths": 22, "assists": 18 },
    "NP":  { "kills": 22, "deaths": 45, "assists": 9 }
  },
  "matches": [
    {
      "date": "2026-03-21",
      "opponent": "naive-piggy",
      "event": "Swiss Round 1",
      "score": "3-0",
      "maps": [
        {
          "map": "Busan",
          "result": "WBG Win",
          "duration": "8:32",
          "ban_WBG": "Zarya",
          "ban_NP": "D.Va",
          "WBG": {
            "tank":   { "player": "Guxue",    "hero": "Domina",
                        "damage_dealt": 12450, "damage_blocked": 8320,
                        "kills": 8, "deaths": 3, "assists": 5, "ult_used": 4 },
            "dps1":  { "player": "Leave",     "hero": "Tracer",
                        "damage_dealt": 18920, "eliminations": 11,
                        "kills": 10, "deaths": 2, "melee": 1, "ult_used": 3 },
            "dps2":  { "player": "shy",       "hero": "Sojourn",
                        "damage_dealt": 22100, "railgun_kills": 6,
                        "kills": 9, "deaths": 4, "ult_charges": 5, "ult_used": 4 },
            "sup1":  { "player": "LeeSooMin", "hero": "Kiriko",
                        "healing": 15200, "damage_dealt": 4200,
                        "kills": 3, "deaths": 2, "ults_given": 5, "ult_used": 5 },
            "sup2":  { "player": "MAKA",     "hero": "Lúcio",
                        "healing": 9800, "damage_dealt": 2100,
                        "kills": 2, "deaths": 3, "sound_barrier": 2, "ult_used": 2 }
          },
          "NP": {
            "tank":   { "player": "Unknown",   "hero": "D.Va",
                        "damage_dealt": 7400, "damage_blocked": 5100,
                        "kills": 4, "deaths": 8 },
            "dps1":   { "player": "Unknown",   "hero": "Tracer",
                        "damage_dealt": 11300, "eliminations": 6,
                        "kills": 5, "deaths": 5 },
            "dps2":   { "player": "Unknown",   "hero": "Sojourn",
                        "damage_dealt": 9800, "railgun_kills": 3,
                        "kills": 4, "deaths": 6 },
            "sup1":   { "player": "Unknown",   "hero": "Kiriko",
                        "healing": 8200, "damage_dealt": 1800,
                        "kills": 2, "deaths": 7 },
            "sup2":   { "player": "Unknown",   "hero": "Lúcio",
                        "healing": 6100, "damage_dealt": 900,
                        "kills": 1, "deaths": 8 }
          }
        }
      ]
    }
  ],
  "hero_frequency": {
    "tank":    { "Domina": 5, "D.Va": 2 },
    "dps":     { "Tracer": 5, "Sojourn": 4, "Cassidy": 2 },
    "support": { "Kiriko": 5, "Lúcio": 3, "Brigitte": 2 }
  },
  "player_match_totals": {
    "Guxue":    { "team": "WBG", "hero": "Domina", "kills": 8,  "deaths": 3,  "damage_dealt": 12450, "damage_blocked": 8320, "healing": 0 },
    "Leave":    { "team": "WBG", "hero": "Tracer",  "kills": 10, "deaths": 2,  "damage_dealt": 18920, "damage_blocked": 0,    "healing": 0 },
    "shy":      { "team": "WBG", "hero": "Sojourn", "kills": 9,  "deaths": 4,  "damage_dealt": 22100, "damage_blocked": 0,    "healing": 0 },
    "LeeSooMin":{ "team": "WBG", "hero": "Kiriko",  "kills": 3,  "deaths": 2,  "damage_dealt": 4200,  "damage_blocked": 0,    "healing": 15200 },
    "MAKA":     { "team": "WBG", "hero": "Lúcio",   "kills": 2,  "deaths": 3,  "damage_dealt": 2100,  "damage_blocked": 0,    "healing": 9800 }
  },
  "last_updated": "<ISO8601>",
  "source_url": "https://owtv.gg/matches/1233"
}
```

**提取规则（OWTV matches/{id} 专用）：**
- `match_id`：从 URL 直接提取（如 `/matches/1233` → `match_id = "1233"`）
- `team_id`：从页面标题或内容中的战队名推断，转换为 kebab-case
- `overall_stats`：整场比赛的队伍合计 K/D/A（OWTV matches/{id} 通常含此数据）
- 每位选手 `player_match_totals{}`：字段说明：

| 字段 | 说明 | 常见来源 |
|---|---|---|
| `damage_dealt` | 造成伤害 | 选手面板 |
| `damage_blocked` | 抵挡伤害（坦克） | 选手面板 |
| `healing` | 治疗量（辅助） | 选手面板 |
| `kills` / `deaths` | 击杀 / 死亡 | 选手面板或队伍统计 |
| `assists` | 助攻 | 选手面板 |
| `eliminations` | 消灭数（部分页面显示） | 选手面板 |
| `ults_given` | 给出的终极技能（辅助） | OWTV 特有 |
| `ult_used` | 终极技能使用次数 | 选手面板 |
| `melee` | 近战击杀 | 选手面板 |
| `sound_barrier` | 声屏障使用次数 | OWTV/Lúcio 特有 |

- `hero_frequency`：汇总该场比赛所有地图的各英雄出场次数
- 若页面不含详细英雄数据 → web_fetch 搜索 recap slug → 抓 recap 文章
- 若 recap 也无 → 标记 `"hero_picks_available": false`，只写入赛果
- **OWTV matches/{id} 必抓字段**（优先级高）：`overall_stats`、`maps[].result`、`maps[].score`
- **OWTV matches/{id} 选抓字段**（若页面提供）：`damage_dealt`、`healing`、`damage_blocked`、`player_match_totals{}`

**搜索 OWTV recap 文章（无 matches/{id} 时）：**
```json
web_fetch({"url": "https://duckduckgo.com/html/?q=site:owtv.gg+OWCS+2026+China+Stage+1+recap"})
```
然后从搜索结果中提取 slug，拼凑完整 URL：
```
https://owtv.gg/news/{slug-from-search-results}
```

**完整 OWTV 数据抓取工作流（优化版 v2）：**

```
# === Step 1: 发现赛事 ID ===
# 查 references/owtv-tournament-ids.md 已知赛事 ID
# 或搜索：web_fetch("https://duckduckgo.com/html/?q=site:owtv.gg/tournaments+China+Stage+1+OWCS+2026")

# === Step 2: 批量发现比赛 ID ===
# OWTV 比赛 ID 连续递增，已知一个 ID 后向相邻数字探测
# 示例（China Stage 1 首日）：
for ID in 1228 1229 1230 1231 1232 1233 1234 1235; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://owtv.gg/matches/$ID" --max-time 3)
  [ "$STATUS" = "200" ] && echo "发现比赛: $ID"
done

# === Step 3: 批量抓取每场比赛详情 ===
extract_content_from_websites(tasks=[
  {"url": "https://owtv.gg/matches/1230", "prompt": "Extract all player stats for every map: role, player ID, Elim, Ast, Dth, DMG, Heal, Mit"},
  {"url": "https://owtv.gg/matches/1231", "prompt": "Extract all player stats for every map..."},
  {"url": "https://owtv.gg/matches/1232", "prompt": "Extract all player stats for every map..."},
  {"url": "https://owtv.gg/matches/1233", "prompt": "Extract all player stats for every map..."}
])

# === Step 4: 写入 hero_picks 缓存 ===
# 文件名：hero_picks/{event-id}-day{n}.json（格式见 schema.md v2.0）

# === Step 5: 运行选手数据分析器 ===
python3 references/player_stats_summarizer.py hero_picks/{event-id}-day{n}.json
# → 输出 MPS 排名（公平局均评选，胜方×1.10加成）
```

---

### ⚡ 优化 4：选手数据分析器（公平 MPS 评选）

OWTV 面板数据（Elim / Ast / Dth / DMG / Heal / Mit）局数不同，直接比总量不公平。
使用 `references/player_stats_summarizer.py` 进行**公平局均 MPS 评选**。

**运行命令：**
```bash
python3 references/player_stats_summarizer.py hero_picks/owcs-2026-china-s1-day1.json
python3 references/player_stats_summarizer.py hero_picks/owcs-2026-china-s1-day1.json --json
# → --json 额外输出结构化 JSON 结果
```

---

### 🏆 公平 MPS 评选机制（最佳选手评选算法）

#### 问题：为什么不能直接比总量？

| 比赛结果 | 局数 | 影响 |
|---|---|---|
| 3-0 横扫 | 3局 | 总量最低，但每局压制力可能最强 |
| 3-2 险胜 | 5局 | 总量最高，但每局效率不一定最优 |

→ 直接比总量 → **对 3-0 队伍严重不公平**

#### 解决方案：Per-Map Normalization

```
每项统计 ÷ 比赛总局数 → 局均统计
例：Wen 212 elim ÷ 5局 = 42.4 elim/m（5局总量仍然领先）
    SUNZO 102 elim ÷ 3局 = 34.0 elim/m（3局总量较少但局均不差）
```

#### MPS 公式（v3 — 角色核心指标设计）

**设计原则：每个角色有且只有一个核心指标，其他指标仅作辅助背景。**

```
┌─────────────────────────────────────────────────────────────┐
│  Tank 核心 = Damage Blocked（Mits/阻挡伤害）               │
│  DPS  核心 = Damage Dealt（伤害输出）                     │
│  Sup  核心 = Healing（治疗量）                           │
│  通用次要 = Eliminations（击杀贡献）                      │
│  通用背景 = KDA（存活效率）                              │
└─────────────────────────────────────────────────────────────┘

Step 1 — Per-Map Normalization
  所有指标 ÷ 比赛总局数 → 局均统计（消除 Bo3/Bo5 总量差异）

Step 2 — Z-Score 归一化
  每项指标 ÷ 该指标全局最大值 → [0, 1] 范围，角色内直接可比

Step 3 — 角色专属 MPS 加权
  Tank MPS = 0.50 × blk_norm + 0.30 × elim_norm + 0.20 × kda_norm
  DPS  MPS = 0.50 × dmg_norm  + 0.30 × elim_norm + 0.20 × kda_norm
  Sup  MPS = 0.50 × heal_norm + 0.30 × elim_norm + 0.20 × kda_norm

Step 4 — 胜方 ×1.10 加成
```

#### 胜方 ×1.10 加成

```
获胜队伍的选手 MPS × 1.10
→ 鼓励赢比赛，也让 3-0 横扫队伍的选手获得公正评价
→ 防止"输方数据好看但没意义"的情况
```

#### 排名规则

1. **分位置独立排名**：Tank / DPS / Support 各自独立排序
2. **全场总榜**：所有选手按 MPS 混合排序，取 Top 10
3. **输出**：每位置 Top 5 + MPS 详细分解（击杀/m、伤害/m、KDA、局数）

#### MPS v3 排名表示例

```
  🛡️ Tank — 核心：阻挡伤害
  1. Wen (homie-e)        MPS=0.9325 | 阻挡伤害 24,261/m | ✅胜
  2. feiyang (milk-tea)   MPS=0.7603 | 阻挡伤害 25,281/m
  3. LiGe (all-gamers)   MPS=0.6054 | 阻挡伤害  7,758/m | ✅胜

  💥 DPS — 核心：伤害输出
  1. Pineapple (jdg)    MPS=0.9128 | 伤害输出 23,940/m | ✅胜
  2. fari (homie-e)    MPS=0.8336 | 伤害输出 19,069/m | ✅胜
  3. BABAYAGA (SV)      MPS=0.7656 | 伤害输出 25,208/m

  💚 Sup — 核心：治疗量
  1. Unkn0w (homie-e)   MPS=0.9084 | 治疗量 28,415/m | ✅胜
  2. Remedy (homie-e)   MPS=0.8072 | 治疗量 25,995/m | ✅胜
  3. Diya (milk-tea)    MPS=0.6528 | 治疗量 26,286/m
```

> **为什么 feiyang 阻挡/m（25,281）比 Wen（24,261）还高，但 MPS 更低？**
> → 归一化后 Wen 击杀参与度（elim_n=0.93）远高于 feiyang（elim_n=0.65）
> → Tank MPS = 0.50×blk_n + 0.30×elim_n + 0.20×kda_n
> → Wen: 0.48+0.28+0.09=**0.85** > feiyang: 0.50+0.19+0.07=**0.76**
> → MPS 综合了角色核心职责（阻挡伤害）+ 击杀贡献 + 存活效率三维度

---

## 浏览器抓取失败时

```
方案1: 换用 Chrome profile（可能自带 cookie 绕过部分限制）
  # 方案2: 截图 + images_understand OCR
# （Playwright 脚本已自动截图，路径在输出 JSON 的 screenshot 字段）
images_understand(image_info=[{file: "<截图路径>", prompt:"提取表格中所有数据"}])

方案3: web_fetch 调搜索 URL（multi-search-engine skill，无需 API key）
  web_fetch({"url": "https://www.google.com/search?q=site:liquipedia.net/overwatch+OWCS+2026+China+Stage+1+roster"})
  支持 17 种搜索引擎，详见 /references/multi-search-engine/SKILL.md

方案4: OWTV matches/{id} 逐场抓取（无 recap 文章时的降级方案）
  → 先 web_fetch("https://owtv.gg/matches") 获取所有 match-id
  → 再逐场 web_fetch("https://owtv.gg/matches/{match-id}") 提取英雄数据
  → 仍无数据 → web_fetch 搜索 recap slug → 抓 recap 文章
  Reddit         → 阵容爆料/讨论（无 OWTV 时）
  egamersworld  → 比分/赛程（OWTV/Liquipedia 均无数据时）
```

---

# 第六部分：数据整合与分析方法

## 赛程整合（优化版）

```
OWTV 数据发现路径：
  ① 查 references/owtv-tournament-ids.md → 赛事 ID（如 56 = China Stage 1）
  ② curl 探测相邻 match ID（如 1230~1233）→ 批量发现所有比赛
  ③ extract_content_from_websites 逐场抓取 → hero_picks/{event}-day{n}.json
  ④ python3 references/player_stats_summarizer.py → MPS 公平排名

Liquipedia 数据补充：
  ① Playwright 抓取 Level 2 赛事页 → swiss_standings / teams[]
  ② 对照 OWTV 赛果补全赛程时间
```

**选手数据分析标准流程（OWTV 数据）：**

1. `extract_content_from_websites` 批量抓所有 `https://owtv.gg/matches/{id}` 详情
2. 写入 `hero_picks/{event-id}-day{n}.json`（schema v2.0）
3. `python3 references/player_stats_summarizer.py hero_picks/...json`
4. 输出分位置 Top 5 + 全场 MPS 总榜 Top 10
5. 结合胜负背景（Bo3/Bo5/横扫/险胜）给出文字分析

## 阵容追踪

1. 从赛事主页或战队主页（teams/）提取 `roster` 和 `changes`
2. 对比上一赛季阵容（teams/{id}.json 历史版本）标注变动
3. 标注规范：
   - `↑ 新加入`：在 `changes.new_players` 中列出
   - `↓ 离队`：在 `changes.departed_players` 中列出
   - `留队`：两方均有则不标注

## 实力评估（输出供前瞻使用，不写入缓存）

1. 汇总各队 `roster`（按 teams/ schema）
2. 评估维度：
   - 选手知名度 + 历史数据（查 players/）
   - 大赛经验（OWCS 国际赛/OWWC 经历）
   - 阵容深度（roster 人数，中韩比例）
   - 沟通成本（韩援数量 → `roster[].nationality === "KR"` 统计）
3. 输出 5 星制分级（写入独立文件 `analysis/{event-id}-preview.json`）

## 奖金/历史排名

1. 抓取 `Portal:Statistics/Player_earnings` → 写入 `earnings/player-earnings-{year}.json`
2. 抓取 `Portal:Statistics/Team_earnings` → 写入 `earnings/team-earnings-{year}.json`
3. 按年份/地区/赛事级别筛选，输出结构化排名

---

# 第七部分：输出格式模板

## 赛事速报（tournaments/ 数据 → 人类可读）

```
[赛事名称] [开始日期–结束日期]

赛制：[瑞士轮 Bo3 / 循环赛 Bo3 / 淘汰赛 Bo5]
奖金池：[USD金额]
赛区：[China/NA/EMEA/Korea/Asia]

--- 参赛队伍（种子序号）---
1. [战队名]（#种子）
2. [战队名]（#种子）
...

--- 瑞士轮/循环赛 赛程与结果 ---
[日期] [战队A] vs [战队B]  →  [比分]（胜者）
[日期] [战队C] vs [战队D]  →  [比分]（胜者）

--- 淘汰赛 ---
[日期] [战队A] vs [战队B]  →  [比分]（胜者）

--- 最终排名 ---
冠军: [战队名]
亚军: [战队名]
季军: [战队名]
数据来源: [URL] | 抓取时间: [ISO8601]
```

## 阵容卡片（teams/ 数据 → 人类可读）

```
[战队名] | [赛事/赛区]
成立于：[年份] | 赛区：[CN/KR/NA/EMEA]

--- 阵容 ---
TANK:    [选手ID] ([真名] / 🇰🇷🇨🇳)
         [选手ID] ([真名] / 🇰🇷🇨🇳)
DPS:     [选手ID] ([真名] / 🇰🇷🇨🇳)
         [选手ID] ([真名] / 🇰🇷🇨🇳)
         [选手ID] ([真名] / 🇰🇷🇨🇳)
SUPPORT: [选手ID] ([真名] / 🇰🇷🇨🇳)
         [选手ID] ([真名] / 🇰🇷🇨🇳)

--- 教练组 ---
主教练: [教练ID] ([国籍])
教练:   [教练ID] ([国籍])

--- 本赛季变动 ---
↑ 新加入: [选手ID]（来自 [原战队名]）
↓ 离队:   [选手ID]（加入 [新战队名] / 退役）
数据来源: [URL] | 抓取时间: [ISO8601]
```

## 前瞻分析（analysis/ 数据）

```
[赛事名称] 前瞻

参赛队伍：X支
赛制：瑞士轮 [日期] → 淘汰赛 [日期]
赛制：[X] vs [X] Bo[数字]

--- 实力分级 ---
第一梯队: [战队名] ★★★★★ — 头号热门
第二梯队: [战队名] ★★★★☆ — 冲冠梯队
第三梯队: [战队名] ★★★☆☆ — 中游竞争者
搅局者:   [战队名] ★★☆☆☆

--- 核心看点 ---
[看点1：具体选手对位 / 战术体系 / 历史交锋]
[看点2]

--- 预测 ---
冠军候选: [战队名]
黑马: [战队名]
最关键对位: [选手A] vs [选手B]
```

## 选手数据卡（players/ 数据 → 人类可读）

```
[选手ID] | [真名]
位置: [Tank/DPS/Support] | 国籍: [🇨🇳🇰🇷...]
当前战队: [战队名]

--- 职业生涯 ---
历史战队: [战队列表，含年份]
主要成就:
  🏆 [赛事名称] ([年份]) — 冠军
  🏆 [赛事名称] ([年份]) — 亚军
累计奖金: [USD金额]

--- 代表英雄 ---
[英雄名]、[英雄名]、[英雄名]

--- 最近转会 ---
[选手ID]: [原战队] → [新战队]（[日期]）
数据来源: [URL] | 抓取时间: [ISO8601]
```

---

# 第八部分：泛用性提示

- **必须用 Playwright Scraper 访问 Liquipedia**：`extract_content_from_websites` / `curl` 均触发 403
- **所有写入缓存的数据必须对齐 schema.md 字段名**，不要自创字段
- 不限年份：URL 中年份替换如 `2025`、`2024` 同样有效
- 不限赛区：China / NA / EMEA / Korea / Asia/Pacific 路径均可通用
- 不限赛事：OWCS / OWL / OWWC / Collegiate / B-Tier 替换路径名即可
- 不确定 URL 时：`web_fetch({"url": "https://www.google.com/search?q=site:liquipedia.net/overwatch+[关键词]"})`
- 浏览器抓取失败时：换 Chrome profile → 截图 OCR → Google 摘要 → OWTV.gg/Reddit
- 中文语境：中文战队名对应英文名（如"微博电竞"→ Weibo Gaming），两种名称均可查询
- 缓存优先：每次成功抓取后立即按 schema 保存，减少重复访问
- **选手数据分析脚本（OWTV 面板数据专用）**：`python3 references/player_stats_summarizer.py <hero_picks.json>` → 公平局均 MPS 排名，无需手动计算
  - 参考：`references/owtv-tournament-ids.md`（OWTV 赛事 ID 速查）
  - 参考：`references/owtv-match-discovery.md`（比赛 ID 批量发现脚本）
  安装：`clawhub install multi-search-engine --dir ~/.openclaw/skills/`
  用法：`web_fetch({"url": "https://www.google.com/search?q=site:liquipedia.net/overwatch+[关键词]"})`
  示例：`web_fetch({"url": "https://duckduckgo.com/html/?q=site:owtv.gg+Milk+Tea+roster"})`
- **性能技巧**：多个 URL 并行运行 playwright-stealth.js（后台 `&` 并发）；stealth 遇到 Cloudflare 时换 headful 模式
