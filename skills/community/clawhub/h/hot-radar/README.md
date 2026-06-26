# 📡 热点收集雷达 - 完整使用文档

> 多平台热点追踪 + 趋势分析 + 竞品监控 + AI 日报生成

## 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4 jieba
```

### 2. 初始化飞书 Token（用于飞书推送和多维表格同步）

```bash
node scripts/read-uat-token.js
```

### 3. 运行

```bash
# 每日采集 + 分析 + 日报
python skills/hot-radar/hot-radar.py --mode daily

# 每日采集 + 同步到飞书多维表格 + 生成日报
python skills/hot-radar/hot-radar.py --mode daily --sync-bitable

# 完整：采集 + 同步飞书 + 推送飞书
python skills/hot-radar/hot-radar.py --mode daily --sync-bitable --notify
```

---

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--mode daily` | 每日采集 + 分析 + 生成报告 | 默认 |
| `--sync-bitable` | 同步到飞书多维表格 | 每日定时任务用 |
| `--notify` | 推送飞书消息卡片 | 日报通知 |
| `--mode analyze --date 2026-05-23` | 重新分析指定日期 | 调试用 |
| `--mode compare --platforms zhihu,weibo` | 跨平台对比 | 专题分析 |
| `--mode keywords` | 按关键词过滤 | 竞品监控 |

---

## 工作流程

```
每日定时 / 手动触发
        │
        ▼
  crawler.py  →  并发爬取各平台热搜
        │
        ▼
  analyzer.py →  话题聚类 + 生命周期 + 共鸣度评分
        │
        ├─→ reporter.py  →  生成 Markdown 日报
        │
        └─→ bitable_sync.py  →  同步到飞书多维表格（--sync-bitable）
        │
        ▼
  notifier.py →  推送到飞书（--notify）
```

---

## 核心分析模型

### 生命周期判断

| 阶段 | 判断依据 | PM 建议 |
|------|---------|---------|
| 新兴 | 单平台出现，无持续信号 | 跟踪关注 |
| 爆发中 | 3平台共振 或 多个爆发信号词 | 抓紧借势 |
| 持续发酵 | 多平台 + 持续讨论信号 | 深度内容 |
| 衰减中 | 降温信号词 或 单平台 | 盘点总结 |

### 共鸣度评分（0-10分）

```
共鸣度 = min(10, 热度值/100万 × 平台权重 + 平台覆盖率×3)
```

平台权重：知乎1.2 / 微博1.0 / 抖音0.9

### 话题聚类

使用 jieba 分词，提取关键词，合并相似话题（关键词重叠≥30%）

---

## 配置

### 关键词配置 (config/keywords.json)

```json
{
  "competitors": ["喜马拉雅", "蜻蜓FM", "荔枝"],
  "industry": ["AI", "大模型", "AIGC", "播客"],
  "alerts": ["下架", "被罚", "宕机", "数据泄露"]
}
```

### 平台配置 (config/platforms.json)

可调整各平台的权重和采集数量

---

## 文件结构

```
skills/hot-radar/
├── hot-radar.py          ← 主入口
├── modules/
│   ├── crawler.py         ← 多平台爬虫
│   ├── analyzer.py        ← 话题分析
│   ├── reporter.py        ← 日报生成
│   └── notifier.py       ← 飞书推送
├── config/
│   ├── keywords.json      ← 关键词配置
│   └── platforms.json     ← 平台配置
├── data/                  ← 原始数据存档
│   └── YYYY-MM-DD.json
└── reports/              ← 日报存档
    └── YYYY-MM-DD.md
```

---

## 与「每日热点追踪」Skill 的区别

| | 每日热点追踪 | 热点收集雷达 |
|---|---|---|
| 定位 | 数据抓取 | 深度分析 |
| 输出 | JSON + 飞书表格 | Markdown 日报 |
| 分析 | 无 | 生命周期、共鸣度、话题聚类 |
| 竞品监控 | ❌ | ✅ 关键词匹配 |
| PM 洞察 | ❌ | ✅ |
| 推送 | 飞书卡片 | 飞书卡片 |
