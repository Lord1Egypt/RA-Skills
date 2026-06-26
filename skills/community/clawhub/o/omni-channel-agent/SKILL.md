---
name: omni-channel-agent
description: 全渠道选品 Agent — 拉齐社媒端、SEO端、投放端数据，帮助运营同学确定待上线需求。触发词：选品、社媒热点、SEO调研、竞品广告、Facebook Ads、TikTok趋势。
---

# 全渠道选品 Agent

全自动从多个数据源抓取竞品和趋势数据，输出 Slack 格式报告。

## 三大频道 + KOL 雷达

### 🎯 KOL 趋势雷达（核心能力 — 源自趋势方法论文档）

基于《Identifying Global Social Media Trends for AI Agent Development》方法论，
监控 11 个分层 KOL 账户，抓取最新内容并自动评估趋势适配度。

**方法论核心原则：人类直觉 > 数据分析工具**
- 数据有滞后、无法理解"氛围"、充满垃圾数据
- 利基社区（动漫粉、地下舞者、特效化妆师）开创最佳趋势
- 最终判断三要素：视觉区分度 + AI可复制性 + 虚荣心触发

#### 三级账号体系

| 级别 | 账号 | 用途 |
|------|------|------|
| 🔴 T1 潮流引领者 | @cyber0318, @hoaa.hanassii, @thybui.__ | 创造趋势，每天监控 |
| 🟡 T2 快速采用者 | @angelinazhq, @lena_foxxx, @caroline_xdc, @upminaa.cos | 趋势确认信号 |
| 🔵 T3 专业雷达 | @cellow111, @emmawhatstwo, @voulezjj, @sawamura_kirari | 运动捕捉/竞品/编辑 |

#### 自动化能力
- **KOL profile 批量抓取** — 一次 Apify 调用获取所有账号最新内容
- **音频趋势聚合** — 多KOL使用相同音频 = 强趋势信号
- **AI 适配度评估** — 自动打分（传播力/互动率/AI关键词/音频/分享率）
- **趋势评估三问** — 视觉区分度？AI可复制性？虚荣心触发？

#### 五阶段方法论
1. **环境设置** — 克服地理围栏（SIM/VPN/设备语言/时区）
2. **趋势发现** — 观察列表 + 音频驱动跟踪 + 关注列表逆向工程
3. **算法训练** — 训练平台推荐算法（3-5天有序互动）
4. **趋势评估** — 视觉区分度 + AI可复制性 + 虚荣心触发
5. **数据管理** — 核心名单月更 + 趋势记录（视频链接+音频链接+视觉描述）

详细方法论参见: `TREND_METHODOLOGY.md`

### 📱 社媒端（6个数据源）
| 数据源 | 工具 | 费用 |
|--------|------|------|
| KOL 雷达(11账号) | Apify `clockworks/tiktok-scraper` profile模式 | Apify 按量 |
| TikTok | Apify `clockworks/tiktok-scraper` | Apify 按量 |
| Instagram | Apify `apify/instagram-scraper` | Apify 按量 |
| YouTube | Apify `streamers/youtube-scraper` | Apify 按量 |
| Reddit | Apify `trudax/reddit-scraper-lite` | Apify 按量 |
| Google Trends | pytrends (免费) | 免费 |

### 🔍 SEO端
| 数据源 | 说明 |
|--------|------|
| Semrush API | 竞品关键词（11个竞品域名） |
| Sitemap | art.myshell.ai 页面去重 |
| Notion Bot DB | 已有 Bot 去重 |

### 📢 投放端
| 数据源 | 说明 |
|--------|------|
| Facebook Ads Library | 通过 Apify `apify/facebook-ads-scraper`，4个查询场景 |

## 环境要求
```
APIFY_TOKEN=...          # Apify API token (必须)
SEMRUSH_API_KEY=...      # Semrush API key (SEO端必须)
NOTION_IMAGE_BOT_TOKEN=... # Notion token (去重用，可选)
```

## 使用方法

```bash
SKILL_DIR=~/.openclaw/workspace/skills/omni-channel-agent

# 全量 Pipeline（KOL雷达+社媒+SEO+投放）
python3 $SKILL_DIR/run_pipeline.py --query "ai filter"

# 单频道
python3 $SKILL_DIR/run_pipeline.py --channel social --query "ai filter"
python3 $SKILL_DIR/run_pipeline.py --channel seo
python3 $SKILL_DIR/run_pipeline.py --channel ads --query "ai photo generator"

# 快速测试（减少数据量）
python3 $SKILL_DIR/run_pipeline.py --test

# 参数说明
--query       搜索关键词（默认 "ai filter"）
--channel     频道选择 all/social/seo/ads（默认 all）
--region      区域 US/EU/ASIA（默认 US）
--max-results 每个源最大结果数（默认 15）
```

## 输出
- `output/full_report_YYYYMMDD_HHMM.txt` — Slack 格式完整报告
- `output/social_*.json` — 社媒原始数据（含KOL雷达 + 音频趋势 + AI适配度评估）
- `output/seo_*.json` — SEO 关键词数据
- `output/ads_*.json` — 广告数据
- `output/all_data_*.json` — 全量合并数据

## 文件结构
```
omni-channel-agent/
├── SKILL.md                # 本文件
├── TREND_METHODOLOGY.md    # 社媒趋势方法论（Lark文档完整版）
├── apify_client.py         # Apify REST API 客户端
├── run_pipeline.py         # 主 Pipeline（KOL雷达+3频道编排）
├── run_all.py              # 社媒端单独运行
├── run_multi_query.py      # 多场景查询
├── sources/
│   ├── kol_radar.py        # 🆕 KOL 雷达（11账号监控+音频聚合+AI评估）
│   ├── tiktok.py           # TikTok via Apify
│   ├── instagram.py        # Instagram via Apify
│   ├── youtube.py          # YouTube via Apify
│   ├── reddit.py           # Reddit via Apify
│   ├── google_trends.py    # Google Trends (pytrends)
│   ├── facebook_ads.py     # Facebook Ads via Apify
│   ├── seo_pipeline.py     # SEO: Semrush + Sitemap + Notion dedup
│   ├── ads_pipeline.py     # 投放: 4个场景
│   └── twitter.py          # Twitter (待修复 token)
├── formatters/
│   └── slack_formatter.py
└── output/                 # 数据输出
```

## 注意事项
- KOL 雷达每次批量抓取 11 个账号，Apify 消耗较大，建议非 test 模式每天 1-2 次
- Instagram 和 Reddit 的 Apify actor 是按量付费的
- Google Trends 有 rate limit，高频调用会 429
- Sitemap 需要 User-Agent header（403 防护）
- Twitter API 的 token 需要官方 Bearer token，当前 OpenTwitter JWT 不兼容
- **趋势最终判断需人类直觉** — AI 评分仅供初筛，视觉效果/氛围/文化细微差别只有人眼能捕捉
