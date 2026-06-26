# 📡 热点收集雷达

多平台热点追踪 + 趋势分析 + 竞品监控 + AI 日报生成。

> 超越单纯的数据抓取，从**产品经理视角**分析热点的生命周期、话题共鸣度与跨平台传播路径。

## 何时使用本 Skill

- 用户说：**「热点雷达」「竞品热点」「行业日报」「热点分析」「生成日报」**
- 需要追踪特定关键词在多平台的热度变化
- 需要生成结构化的每日热点报告
- 需要按领域（科技/娱乐/财经等）筛选热点

## 核心功能

| 功能 | 说明 |
|------|------|
| 多平台爬取 | 知乎/微博/抖音热搜，知乎热榜 |
| 话题聚类 | 自动将相似话题归类（如多个 AI 相关话题合并） |
| 生命周期判断 | 新兴 / 爆发中 / 持续发酵 / 衰减中 |
| 共鸣度评估 | 热度值 × 平台权重 × 平台覆盖率 综合评分 |
| 跨平台传播 | 识别同一事件在不同平台的反应差异 |
| **PM 选题建议** | **自动从话题中提炼选题角度 + 内容切入点 + 适合形式** |
| **飞书推送** | **推送带选题建议的日报简报到飞书私聊** |

## 文件结构

```
skills/hot-radar/
├── SKILL.md              ← 本文件（Agent 主入口）
├── _meta.json            ← Skill 元数据
├── README.md             ← 完整使用文档
├── hot-radar.py          ← 主程序入口
├── config/
│   ├── keywords.json     ← 关键词配置（竞品词/行业词）
│   └── platforms.json    ← 平台配置
├── modules/
│   ├── crawler.py        ← 多平台爬虫
│   ├── analyzer.py       ← 话题分析与生命周期
│   ├── reporter.py        ← 日报生成器
│   ├── notifier.py       ← 飞书推送
│   └── browser_crawl.py ← tophub 浏览器采集（子 agent 模式）
├── tophub_browser_collect.py ← tophub AI 专题浏览器采集入口
└── crawl_tophub.py      ← 浏览器采集配置
└── data/                 ← 每日原始数据存档
    └── YYYY-MM-DD.json
└── reports/              ← 日报存档
     └── YYYY-MM-DD.md
```

## 快速使用

## tophub AI 专题浏览器采集

tophub.today 的内容通过 JavaScript 动态渲染，HTTP 请求无法获取，必须通过 OpenClaw 浏览器采集。

**当前状态：✅ 已集成** — 浏览器采集数据已合并到每日报告中。

### 数据源

| 平台 | URL | 数据类型 | 条数 |
|------|-----|---------|------|
| 36氪AI | tophub.today/n/x9oz2O1oXb | 创投/行业新闻 | 30条 |
| 量子位 | tophub.today/n/MZd7azPorO | AI行业媒体 | 10条 |
| AIbase | tophub.today/n/ENeYylkeY4 | AI产品日报 | 10条 |
| AI产品榜 | tophub.today/n/proPKWkeq6 | 产品动态 | 10条 |
| PM-AI学习库 | tophub.today/n/DOvnyGpoEB | PM专属内容 | 10条 |
| 掘金AI | tophub.today/n/rYqoXz8dOD | 技术实战 | 10条 |
| 超神经 | tophub.today/n/4MdA863vxD | 学术/开源 | 10条 |

### 采集工作流

**第一步**：在主会话中运行 hot-radar.py 采集已有平台数据
**第二步**：使用 browser 工具逐个访问 tophub 页面，用 evaluate 提取数据
**第三步**：将结果写入 `data/tophub_ai_raw.json`
**第四步**：hot-radar 下次运行时自动读取并合并

### 命令行参数

```bash
python3 skills/hot-radar/hot-radar.py --mode daily
python3 skills/hot-radar/hot-radar.py --mode daily --sync-bitable
python3 skills/hot-radar/hot-radar.py --mode daily --sync-bitable --notify
python3 skills/hot-radar/hot-radar.py --mode keywords
python3 skills/hot-radar/hot-radar.py --mode analyze --date 2026-05-23
python3 skills/hot-radar/hot-radar.py --mode compare --platforms zhihu,weibo
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--mode daily` | 每日热点采集 + 分析 + 生成日报 |
| `--mode keywords` | 按关键词过滤并分析 |
| `--mode analyze` | 对指定日期数据重新分析 |
| `--mode compare` | 跨平台对比 |
| `--sync-bitable` | 同步到飞书多维表格 |
| `--notify` | 同时推送到飞书 |
| `--date YYYY-MM-DD` | 指定分析日期 |

## 热点生命周期模型

```
[新兴] → [爆发中] → [持续发酵] → [衰减中] → [消亡]
  ↑           ↑           ↑           ↑
 新话题出现  3平台共振  多角度讨论  热度持续下滑
```

| 阶段 | 特征 | PM 建议 |
|------|------|---------|
| 新兴 | 单平台出现，相关词少 | 跟踪关注，判断是否跟进 |
| 爆发中 | 3平台同时出现，热度急升 | 内容布局窗口期，抓紧借势 |
| 持续发酵 | 持续出现在热搜，讨论维度增加 | 深度内容或系列内容机会 |
| 衰减中 | 热度下降，但仍有余温 | 内容长尾，可做总结盘点类 |

## 关键词配置

编辑 `config/keywords.json` 配置你的监控关键词：

```json
{
  "competitors": ["竞品A", "竞品B", "竞品C"],
  "industry": ["AI", "大模型", "AIGC", "内容平台"],
  "alerts": ["危机", "下架", "被罚", "宕机"]
}
```

## 报告结构（每日日报）

```markdown
# 📡 热点日报 · 2026-05-23

## ⭐ 跨平台共振话题
### [话题名]
- 平台: 抖音+2平台共振
- 生命周期: 爆发中 / 持续发酵
- 共鸣度: ⭐9.2
- 主题: 航天/AI/体育

## 🔥 热点排行榜（按共鸣度）
| # | 话题 | 平台 | 生命周期 | 共鸣度 |
|---|------|------|---------|--------|
| 1 | 神舟二三三发射 | 抖音 | 🔥爆发中 | ⭐10 |

## 🎯 今日选题建议

### 🔴 第一梯队：必追话题
**话题名**
- 共鸣度：⭐10
- 选题角度：[从PM视角的切入角度]
- 内容切入点：[具体内容方向]
- 适合形式：深度播客 / 短视频
- ⏰ 立即行动，流量窗口期

### 🟡 第二梯队：可跟进话题
...

## 💡 PM 洞察
...

## 📊 平台数据摘要
| 平台 | 热点数 | 最热话题 |
|------|--------|---------|
| 知乎 | 10 | 神舟二三三... |
| 微博 | 10 | ... |
```

**与旧版日报的核心区别：** 自动生成选题建议 + 生命周期判断 + PM视角内容切入点分析

## 依赖

```bash
pip install requests beautifulsoup4 jieba
```

## 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| 知乎热榜 | ✅ 正常 | API 直连，每平台10条 |
| 微博热搜 | ✅ 正常 | 实时热搜接口 |
| 抖音热点 | ✅ 正常 | 公开榜单接口 |
| YouTube热门 | ⚠️ 需配置 | 需 Google Cloud API Key |
| X/Twitter趋势 | ⚠️ 不稳定 | Nitter / Google News RSS fallback |
| Instagram热点 | ⚠️ 需 Cookie | config/instagram.json |
| 今日热榜 | ✅ Google News | tophub.today 有 JS 保护，改用 Google News RSS 聚合 |
| **tophub AI 专题** | ✅ 浏览器采集 | 36氪AI/量子位/AIbase/AI产品榜/PM-AI学习库（通过 OpenClaw 浏览器采集，已集成） |
| **tophub 财经专题** | ✅ 浏览器采集 | 华尔街见闻/雪球/21财经/格隆汇/第一财经（通过 OpenClaw 浏览器采集，已集成） |

**v1.1.0 更新**：新增财经专题热报、浏览器采集 tophub AI/财经专题、独立板块展示、共鸣度对数压缩、历史趋势对比

**启用/停用平台**：编辑 `config/platforms.json` 中的 `enabled` 字段。

**YouTube API Key**：[Google Cloud Console](https://console.cloud.google.com/apis/credentials) → 创建 API Key → 启用 YouTube Data API v3
