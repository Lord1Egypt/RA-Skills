---
name: news-digest
description: "Automatically scrape, process, and generate daily news digests from Chinese news sources. Covers industry dynamics, policy updates, economy, tech, energy, and pricing information. Use when: user asks for daily news summary, news digest, 每日新闻摘要, 新闻汇总, 新闻摘要, or wants to set up automated news monitoring from Chinese news websites. Outputs formatted summaries with source attribution and original links."
version: 1.0.12
---

# News Digest - 每日新闻摘要

Automated pipeline for Chinese news aggregation and digest generation.

## Quick Start (3 步搞定)

```bash
# 第 1 步：安装依赖
pip install requests beautifulsoup4

# 第 2 步：一键初始化（建表 + 插入示例网站 + 关键词）
python scripts/news_digest_v2/init_db.py

# 第 3 步：运行摘要
python scripts/news_digest_v2/run_all_stages.py
```

或者一条命令全部搞定：
```bash
python scripts/news_digest_v2/quick_start.py
```

Output: `.news-digest-out.md` (workspace) + `新闻摘要_YYYYMMDD_HHMMSS.txt` (desktop)

## Architecture

```
Stage 1:   Fetch     →  Scrape websites → Filter → Save to SQLite DB
Stage 2:   Process   →  Deduplicate (≥90% similarity) → Tag keywords
Stage 2.5: LLM       →  Batch LLM summarization (optional, requires API key)
Stage 3:   Output    →  Read LLM summaries (fallback to rule summaries) → Save to files
```

## Setup

### Prerequisites

- Python 3.8+ with: `requests`, `beautifulsoup4`
- SQLite (built-in)

### Initialize Database

Run the init script to create tables and seed with sample data:

```bash
python scripts/news_digest_v2/init_db.py
```

This creates:
- Database tables (articles, monitor_websites, system_keywords, digest_output)
- 10 sample news websites (People.cn, Xinhua, 36Kr, etc.)
- 18 sample keywords (产业, 政策, 经济, 科技, etc.)

Default database path: `news.db` (in the skill directory).
Override with environment variable: `NEWS_DIGEST_DB=/your/path/news.db`

### Customizing Your Sources

After initialization, add or remove websites and keywords via SQL:

```sql
-- Add a website
INSERT INTO monitor_websites (name, url, selector, category, priority)
VALUES ('示例网站', 'https://example.com', 'a', '财经', 1);

-- Add a keyword
INSERT INTO system_keywords (keyword, category, weight)
VALUES ('新能源', 'core', 5);
```

### Core Database Tables

| Table | Purpose |
|-------|---------|
| `articles` | Scraped news articles (title, content, URL, date, keywords, duplicate flag) |
| `monitor_websites` | Monitored websites (name, URL, CSS selector, category, enabled) |
| `system_keywords` | Keywords for relevance scoring (core vs auxiliary, with weight) |
| `digest_output` | LLM-generated summaries (optional) |

## Usage

### Full Pipeline

```bash
python scripts/news_digest_v2/run_all_stages.py
```

Takes ~13 minutes (network + LLM bound).

### One-Command Quick Start

```bash
python scripts/news_digest_v2/quick_start.py
```

Runs init + fetch + process + output in one shot.

### Cron Job Example

```yaml
schedule: "0 20 * * *"  # Daily 20:00
payload:
  run: python scripts/news_digest_v2/run_all_stages.py
  then: read .news-digest-out.md and send to messaging
timeout: 900  # 15 minutes
```

## Output Format

```
【来源：标题】
摘要内容（智能选段，300字以内，包含关键数据和核心事实）
发布时间：YYYY-MM-DD
原文链接：http://...
```

### 摘要质量保证

**不完整句子自动过滤**：
- 摘要末尾以逗号、顿号、分号、冒号等结尾 → 回退截断到上一个句号
- 全文没有句号（整段残缺）→ 直接丢弃，不输出
- 截断时信息损失超过 40% → 整段放弃，宁缺毋滥

**教程/指南类内容全部过滤**：
- 标题或内容包含"教程"、"指南"、"攻略"、"手把手"、"从零开始"等 → 自动排除
- 详见 `rules_config.py` 中 `social` 分类的教程关键词列表

## Key Features

### Smart Summary Extraction (fetcher.py → extract_brief_summary)

Not simple truncation. Each paragraph is scored by:
- **Position**: Lead paragraph +10, top-3 +5 (inverted pyramid journalism)
- **Data density**: Numbers × 2.5
- **Signal words**: 印发/发布/宣布/决定/完成/启动 (+2 each)
- **Entity density**: Organizations, locations (+1 each)
- **Completeness**: Full sentence ending +3

Then filtered: removes image captions, journalist bylines, ads, subtitles, boilerplate.

### 摘要后处理 (formatter.py → clean_summary)

- 电头/记者署名清理（预编译正则，支持新华社、中新网、财联社等）
- 不完整句子过滤：以逗号/顿号/分号结尾 → 回退到上一个句号
- 全文无句号 → 丢弃（不输出残缺内容）

### Filtering Rules (rules_config.py)

Excluded topics: entertainment, social news, violence, crime cases, health/wellness, education, automotive consumer news, science popularization (科普类), animal/archaeology news.

**教程类（全部过滤）**：教程、指南、攻略、入门、自学、从零开始、手把手、保姆级教程、怎么做、如何使用、操作步骤、图文教程、视频教程、科研绘图、PS教程、Illustrator 等。

**企业宣传稿/软文（全部过滤）**：产能突破、全线投产、技术溢出、供应链底气、跨界营销、负面舆情、品鉴官、品牌定位等。

**教育/社会活动/颁奖（全部过滤）**：十佳、颁奖仪式、表彰、职校生、职业院校、评选、杰出代表、工匠精神等。

Invalid keywords: clickbait patterns, advertising, webpage navigation elements.

### Deduplication (similarity.py)

- Jaccard 2-gram similarity
- Threshold: ≥90% → mark as duplicate
- Only one version appears in output

### Date Filtering

- Normal: within 3 days
- Holidays: within 7 days
- No date → discard
- Old URLs (year > 1 year ago) → skip

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEWS_DIGEST_DB` | `news.db` | SQLite database path |
| `NEWS_DIGEST_LLM_API_KEY` | (empty) | LLM API key for Stage 2.5 summarization |
| `NEWS_DIGEST_LLM_BASE_URL` | (empty) | LLM API base URL |
| `NEWS_DIGEST_LLM_MODEL` | `qwen3.6-plus` | LLM model name |

If LLM env vars are not set, Stage 2.5 is silently skipped and rule-based summaries are used instead.

## Files

```
news-digest/
├── SKILL.md
└── scripts/
    └── news_digest_v2/
        ├── __init__.py
        ├── config.py               # DB path, websites, keywords, holidays, LLM config
        ├── database.py             # SQLite operations
        ├── fetcher.py              # Web scraping + smart summary extraction
        ├── filters.py              # Content filtering logic
        ├── formatter.py            # Output formatting + incomplete sentence handling
        ├── init_db.py              # One-click database initialization (NEW in v1.0.1)
        ├── quick_start.py          # One-command full pipeline (NEW in v1.0.1)
        ├── rules_config.py         # Exclusion rules, keywords, dateline patterns
        ├── similarity.py           # Jaccard deduplication
        ├── stage1_fetch.py         # Stage 1 entry (fetch)
        ├── stage2_process.py       # Stage 2 entry (dedup + keywords)
        ├── stage2_5_llm_summary.py # Stage 2.5 (LLM batch summarization)
        ├── stage3_output.py        # Stage 3 entry (read + format + save)
        └── run_all_stages.py       # Full pipeline entry
```

## FAQ

**Q: 安装后跑不起来？**
A: 确保先运行了 `init_db.py` 初始化数据库。没有数据库和示例数据，后续步骤会失败。

**Q: pip install 失败？**
A: 尝试 `pip install --upgrade pip` 后再安装。如果网络问题，使用 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests beautifulsoup4`。

**Q: 某些网站抓取失败？**
A: 正常现象。部分网站有反爬或 SSL 问题，脚本会继续处理其他网站。不影响最终输出。

**Q: 输出是空的？**
A: 检查数据库中是否有数据。运行 `python scripts/news_digest_v2/init_db.py` 重新初始化。

**Q: 如何自定义监测网站？**
A: 通过 SQL 插入 `monitor_websites` 表，字段：name, url, selector, category, priority。

**Q: 数据库会越来越大吗？**
A: 约 30-50 条/天。建议定期清理旧数据，或删除 `news.db` 后重新初始化。

## Performance Notes

- ~5 minutes for full scrape (network I/O bound)
- Some sites may fail (SSL issues, 521 errors, 404s) — pipeline continues
- Recommended cron timeout: 900 seconds
- **数据库是增量追加的**，不会被清空。新新闻按 URL 去重插入（`INSERT OR IGNORE`），旧新闻保留。
- 重复新闻标记 `is_duplicate = 1`，不删除。

## Changelog

### v1.0.12 (2026-06-09)
- **新增 6 类过滤规则**（`rules_config.py`）：
  - 文化活动/精神宣讲：诵读会、宣讲会、科学家精神、阅读角、推广计划、弘扬.*精神等
  - 信用知识科普/问答类：信用知识、百问百答、信用体系、信用记录等
  - 新闻简报/早报类：8点1氪、点早闻、早晚报、每日速递、资讯速览等
- **去重修复**：清理 digest_output 中 is_duplicate=1 的残留条目
- **sync_to_skill.py 修复**：新增 cross_day_dedup.py 到同步列表

### v1.0.11 (2026-06-08)
- **新增人民日报主站监控**：`parse_rmrbhwb` 路由增加 `paper.people.com.cn/rmrb/` 支持（数据库新增 id=47, priority=1）
- **跨天去重修复**：`cross_day_dedup.py` 新增硬规则4（标题互相包含检测）+ Jaccard权重 0.5→0.6
- **header 恢复**：formatter.py 恢复'来源网站: X | 收录新闻: Y 条'格式
- **stage2_5 优化**：SQL查询简化 + 日志优化

### v1.0.10 (2026-06-05)
- **Header 条数修复**：`formatter.py` 中"收录新闻"统计从预过滤数改为实际输出数
  - 旧逻辑：统计 `filtered_news` 长度（排除重复后），但未减去内容类型黑名单过滤的条目
  - 新逻辑：用占位符+后置替换，确保 header 数字与实际输出条数一致
- **标题截断保护**：标题以逗号/顿号结尾时自动补省略号，避免数据库截断误导
- **新增过滤规则 5 类**：
  - 党建历史/纪念性：伟大征程、永放光芒、精神永存、丰碑、铸魂、初心等 17 词
  - 节气科普：节气、农忙、天文专家、正本清源、二十四节气等
  - 官员落马/公诉：提起公诉、受贿案、指定管辖、监察调查等 12 词（同时加入 `corporate_scandal` 分类）

### v1.0.8 (2026-06-05)
- **跨天去重**：新增 `cross_day_dedup.py`，对比最近 3 天历史摘要自动拦截跨天重复新闻
  - 核心算法：标题 Jaccard(0.5) + 数字匹配(0.25) + 内容词重叠(0.25)
  - 硬规则：显著数字不共享 → 直接判 0（自动放行 PMI/CPI 等周期性新闻，无需白名单）
  - 三档判定：≥0.75 拦截 / 0.60~0.75 警告保留 / <0.60 正常通过
- **标题改写规则 9**：参展/出席类标题改为事件主体，IPO/融资/财报等保留公司名
- **禁止编造规则 10**：摘要中所有信息必须来源于原文，不得自行补充外部知识
- **来源数显示修复**：`stage1_fetch.py` 从硬编码 42 改为动态读取 `len(WEBSITES)`
- **GBK 解码增强**：`decode_response()` 已合并入主流程，支持所有已知 GBK 来源

### v1.0.7 (2026-06-01)
- **标题乱码修复**：
  - `fetcher.py` 新增 `decode_response()` 函数，对已知 GBK 编码来源（人民日报海外版）强制使用 GBK 解码，从根源修复 Cyrillic 乱码
  - `stage2_5_llm_summary.py` 新增乱码标题检测，发现乱码时提示 LLM 从正文生成准确标题
  - `formatter.py` 新增乱码标题兜底过滤
- **内容类型黑名单**：
  - 新增 `TITLE_EXCLUDE_KEYWORDS`（评论丨/时评/社评/深度观察/记者观察/招聘/面试/递补/人事任免/讣告/专访等）
  - 新增 `URL_EXCLUDE_PATTERNS`（人民网评论频道等）
  - `formatter.py` 输出时自动跳过非硬新闻类型
- **推荐超时**：900s→1200s（实测 LLM 总结 50 条 + 抓取总耗时 ~1150s）

### v1.0.6 (2026-05-29)
- **新闻源增至 46 个**（45 启用，1 个"新华每日电讯"禁用）
- **LLM 模型修复**：默认模型从 `qwen-plus`（不存在，400 错误）改为 `qwen3.6-plus`
- **LLM_BATCH_SIZE**：35→50，与 MAX_OUTPUT_COUNT 一致
- **来源数显示修复**：输出头部"来源网站"从动态统计改为固定 46
- **新增过滤规则**：`corporate_pr`（企业宣传稿/软文）+ `education_social`（教育/颁奖/评选）
- **推荐超时**：600s→900s（因 LLM 总结 50 条耗时增加）
- **飞书队列清理**：不再自动写入飞书

### v1.0.5 (2026-05-28)
- **新增新闻源**：安徽日报、人民日报海外版、新华每日电讯（42→45个启用源）
- **MAX_OUTPUT_COUNT**：35→50条
- **新增关键词**：十五五、标准、纲要、公报、全覆盖、创新药、芯片、测评、公共服务（12个）
- **fetcher.py 兼容修复**：4处相对导入改为 try/except fallback，支持直接运行和包导入
- **中国工信网超时**：10秒→30秒
- **数据库**：新闻源从 SQLite 加载，关键词从数据库读取

### v1.0.4 (2026-05-25)
- **标题清理**：自动去除标题首尾的多余符号（如中点 `·`、空格）
- **输出排序优化**：权威来源（人民网/新华网等）按级别升序排列，同级别按时间倒序
- **过滤规则增强**：新增艺术展览/书画捐赠过滤词（避免非产业类文化新闻干扰）
- **权威选文修复**：修正文章数 <35 时未排序的 Bug

### v1.0.3 (2026-05-22)
- **央广网独立解析器** (`parse_cnr`): 央广网页面标题和正文在同一 `<a>` 标签内，新增独立解析器只取 `<strong>` 作为标题，避免标题+正文混一起导致标题过长被过滤
- **权威来源优先选文**: 阶段 2.5（LLM 批量总结）和阶段 3（输出）都应用权威来源保底策略，每个权威来源（人民网、新华网、央广网、经济日报、科技日报、科学网、中国科技网、科创版日报、中国经济网）至少入选 2 条，避免被中国经济网和中宏网等高产源淹没
- **新华网子频道归并**: 新华能源、新华科创、新华时政、新华汽车等子频道统一归并到"新华网"来源
- **社会新闻过滤增强**: 新增交通违法/行政处罚类社会新闻过滤词（罚款、行拘、拘留、交警、变造号牌等）
- **编码检测优化**: 央广网等 GB2312 编码网站从 HTML `<meta>` 标签检测编码，提高抓取成功率

### v1.0.1 (2026-05-06)
- Added `init_db.py` for one-click database initialization with sample data
- Added `quick_start.py` for one-command full pipeline
- Simplified SKILL.md installation guide to 3 steps
- Added FAQ section
- Updated example websites to 10 mainstream Chinese news sources

### v1.0.0 (2026-05-05)
- Initial release
