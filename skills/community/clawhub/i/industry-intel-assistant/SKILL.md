---
name: industry-intel-assistant
description: 行业情报收集与分析助手。自动监控特定行业动态、抓取热点资讯、生成结构化情报简报，并支持多渠道推送。当用户需要：监控某行业最新动态、追踪竞品消息、抓取AI/科技/电商等行业情报、生成每日/每周情报简报、搭建企业级资讯分发体系时使用此技能。核心功能：(1) Tavily搜索获取行业资讯 (2) 结构化简报生成 (3) 多通道推送（企业微信/飞书/钉钉） (4) 定时任务编排。
---

# Industry Intel Assistant

行业情报收集与分析助手。自动监控特定行业动态，生成结构化简报并推送到指定渠道。

## 核心能力

1. **Tavily 搜索** — 调用 Tavily API 获取指定行业/关键词的最新资讯
2. **简报生成** — 将搜索结果整理为结构化情报简报（标题 + 摘要 + 来源链接）
3. **多渠道推送** — 支持推送到企业微信、飞书、钉钉等平台
4. **定时编排** — 支持 Cron 定时任务，实现每日/每周自动化情报推送

## 快速开始

### 基本搜索

```bash
# 搜索特定行业资讯，返回5条结果
python3 scripts/tavily_industry_search.py "AI大模型 最新动态" --max-results 5
```

### 生成简报并推送

```bash
# 搜索 + 生成中文简报
python3 scripts/generate_intel_report.py --query "跨境电商 2026 动态" --max-results 8 --language zh
```

### 推送到企业微信

```bash
python3 scripts/push_to_wecom.py --report-file ./assets/latest_report.md --channel wecom
```

## 脚本说明

### scripts/tavily_industry_search.py

行业资讯搜索脚本。

```bash
python3 scripts/tavily_industry_search.py "<关键词>" \
  --max-results <1-10> \
  --topic <general|news> \
  --depth <basic|advanced>
```

**参数说明：**
- `query`: 搜索关键词，支持行业、竞品、话题组合
- `--max-results`: 返回结果数量，默认 5
- `--topic`: 搜索范围，general=全网，news=最近7天新闻
- `--depth`: 搜索深度，basic=快速(1-2s)，advanced=深度(5-10s)

**环境变量：**
- `TAVILY_API_KEY`: Tavily API Key（格式: tvly-xxx）

**返回：** JSON 格式搜索结果，包含 title、url、content、score

### scripts/generate_intel_report.py

生成结构化情报简报。

```bash
python3 scripts/generate_intel_report.py --query "<行业关键词>" \
  --max-results <数量> \
  --language <zh|en> \
  --output <输出文件路径>
```

**输出格式：**
```
# [行业] 情报简报 — YYYY-MM-DD

## 今日要点
- 要点1
- 要点2

## 热门资讯
1. [标题](链接) — 摘要
2. [标题](链接) — 摘要
...

## 来源
- [来源1](链接)
- [来源2](链接)
```

### scripts/push_to_wecom.py

推送简报到企业微信。

```bash
python3 scripts/push_to_wecom.py --report-file <文件路径> --channel <wecom|feishu|ddingtalk>
```

**前置要求：**
- 企业微信插件已配置（OpenClaw wecom 插件已启用）
- 推送目标为企业内部群或用户

### scripts/schedule_intel.py

创建定时情报推送任务。

```bash
python3 scripts/schedule_intel.py \
  --query "<关键词>" \
  --schedule "0 9 * * *" \
  --channel <wecom|feishu|ddingtalk> \
  --timezone "Asia/Shanghai"
```

使用 OpenClaw cron 系统创建每日定时推送任务。

## 典型使用场景

### 场景1：每日 AI 行业简报

```bash
python3 scripts/generate_intel_report.py \
  --query "AI大模型 GPT Claude Gemini 生成式AI 最新动态" \
  --max-results 8 \
  --language zh \
  --output ./assets/daily_ai_report.md
```

### 场景2：竞品监控

```bash
python3 scripts/tavily_industry_search.py "竞品名称 最新消息 融资 动态" --topic news --max-results 10
```

### 场景3：跨境电商情报

```bash
python3 scripts/generate_intel_report.py \
  --query "跨境电商政策 平台动态 热门品类 2026" \
  --max-results 8 \
  --language zh \
  --output ./assets/ecommerce_intel.md
```

## 配置说明

### Tavily API Key

获取方式：
1. 访问 https://tavily.com 注册账号
2. 在 Dashboard 生成 API Key（格式: tvly-xxx）
3. 配置到 OpenClaw：`openclaw config set skills.entries.tavily.apiKey "tvly-xxx"`

### 多渠道推送

企业微信/飞书/钉钉需在 OpenClaw 中配置对应插件，参考各平台插件配置文档。

## 进阶用法

### 自定义搜索关键词

可组合多个关键词提升搜索精度：
- `"AI大模型 最新进展"` — 大模型行业动态
- `"竞品名称 融资 上市 动态"` — 竞品追踪
- `"行业政策 法规 2026"` — 政策解读

### 与知识库结合

可将简报内容自动存入企业知识库：
1. 先生成简报
2. 使用知识库技能（knowledge-curator）将内容归档
3. 建立历史情报索引

### 自动化工作流

利用 OpenClaw cron 实现完全自动化：
1. 每日定时触发简报生成
2. 自动推送到指定渠道
3. 异常时发送告警通知
