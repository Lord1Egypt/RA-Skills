---
name: news-brief
description: "Daily Chinese news brief from top global sources (Reuters, Bloomberg, TechCrunch, FT, BBC). Pick up to 3 categories, run setup.py once, get structured briefs every morning. 每日新闻简报，权威来源，一键配置。"
version: "1.0.3"
author: ""
license: MIT
requires:
  env:
    - SERPER_API_KEY     # 必填：serper.dev 获取，免费额度2500次/月
    - DEEPSEEK_API_KEY   # 必填：platform.deepseek.com 获取，极低费用
  python: ">=3.9"
  packages:
    - requests
---

# News Brief Skill

> 每天早上自动生成你的专属新闻简报，来源全部是 Reuters、Bloomberg、TechCrunch 等全球顶级媒体，绝不使用小型网站。

## 它能做什么

- 📰 **12个分类**：时政 / 经济 / 社会 / 国际 / 科技 / 体育 / 文娱 / 军事 / 教育 / 法治 / 环境 / 农业，自由组合最多3个
- 🌍 **双语来源**：同时抓取国际媒体（英文）和国内媒体，DeepSeek 自动翻译+摘要
- ⏰ **定时推送**：配置一次，每天固定时间自动运行
- 🛡 **权威媒体**：Reuters、Bloomberg、FT、BBC、TechCrunch、AP News 等，不用担心来源质量
- 💰 **极低费用**：每月约 ¥25（Serper + DeepSeek），Serper 有免费额度每天1次够用一年

## 为什么选 news-brief

| | news-brief | 普通RSS简报 |
|---|---|---|
| 新闻来源 | Google新闻精选，顶级媒体 | RSS源质量参差不齐 |
| 分类配置 | 12类自由组合 | 固定分类 |
| 配置方式 | setup.py 向导，3分钟搞定 | 手动编辑配置文件 |
| 内容处理 | AI验证时效+翻译+摘要 | 原始标题堆叠 |

## 快速开始

### 1. 配置 API Keys

在 OpenClaw 环境变量中设置：

```bash
SERPER_API_KEY=你的Serper密钥      # 免费：google.serper.dev
DEEPSEEK_API_KEY=你的DeepSeek密钥  # 极低费用：platform.deepseek.com
```

### 2. 编辑 config.yaml

```yaml
categories:
  - 科技    # 第1类（必填）
  - 经济    # 第2类（可选）
  - 国际    # 第3类（可选）
```

**可选分类：** 时政 / 经济 / 社会 / 国际 / 科技 / 体育 / 文娱 / 军事 / 教育 / 法治 / 环境 / 农业

### 3. 运行

```bash
python run.py
```

输出示例：
```
【今日简报】2026/3/17  科技 · 经济 · 国际

📌 今日概览
英伟达宣布新一代AI芯片，中国央行下调LPR，巴以停火谈判陷入僵局。

━━━━━━━━━━━━━━━━━━━━
🔬 科技（5条）
━━━━━━━━━━━━━━━━━━━━
1. 英伟达发布Blackwell Ultra芯片，性能较上代提升40%
   来源：The Verge｜2026/3/17｜美国
   英伟达在年度GTC大会上发布...
...
```

## 定时运行（可选）

```bash
# 每天早8点自动运行
0 8 * * * cd /path/to/skill && python run.py >> logs/daily.log 2>&1
```

## 费用说明

| API | 免费额度 | 超出费用 |
|-----|---------|---------|
| Serper | 2500次/月 | $50/1000次 |
| DeepSeek | - | 约¥0.02/次简报 |

每天运行1次，Serper月费用约$3，DeepSeek约¥0.6，**合计每月约¥25**。

## 新闻来源

| 分类 | 国际权威媒体 | 国内权威媒体 |
|------|------------|------------|
| 时政 | Reuters, AP News | 新华社, 人民网 |
| 经济 | Bloomberg, FT | 财联社, 第一财经 |
| 社会 | BBC, CNN | 澎湃新闻, 南方都市报 |
| 国际 | Reuters, AP News | 环球时报, 参考消息 |
| 科技 | TechCrunch, The Verge | 36氪, 虎嗅 |
| 体育 | ESPN, BBC Sport | 懂球帝, 腾讯体育 |
| 文娱 | Variety, Hollywood Reporter | 娱乐资本论 |
| 军事 | Defense News, Reuters | 观察者网 |
| 教育 | Times Higher Ed | 中国教育报 |
| 法治 | Reuters Legal | 法制日报 |
| 环境 | The Guardian | 财新环境 |
| 农业 | Reuters Agriculture | 农民日报 |

## 文件结构

```
news-brief/
├── SKILL.md      # 本文件
├── config.yaml   # 用户配置（只改这里）
├── run.py        # 一键运行入口
├── fetch.py      # 新闻抓取模块
├── brief.py      # 简报生成模块
└── logs/         # 运行日志（自动创建）
```
