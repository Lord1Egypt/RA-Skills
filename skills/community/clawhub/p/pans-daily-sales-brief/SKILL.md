---
name: pans-daily-sales-brief
description: |
  AI算力销售每日简报生成器。自动汇总待跟进客户、到期合同、新线索和竞品动态。
  维护客户pipeline数据，生成每日工作简报。
  触发词：销售简报, 每日报告, 客户跟进, pipeline, 销售日报, daily brief, sales report
---

# AI算力销售每日简报生成器

## 功能概述

自动汇总每日销售工作要点，包括：
- 📋 今日待办：需要今天联系的客户
- ⚠️ 即将到期：7天内到期的合同
- 🆕 新线索：最近7天新增的线索
- 💰 业绩概览：本月成交额、pipeline金额、转化率
- 🔍 竞品动态：通过SearXNG搜索竞品新闻

## 使用方法

### 生成每日简报
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py
```

### 指定日期
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --date 2024-01-15
```

### 添加客户
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --add-client '{"company":"AI Startup","stage":"初步接洽","next_contact":"2024-01-20","notes":"对H100感兴趣"}'
```

### 添加合同
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --add-contract '{"client":"AI Startup","amount":500000,"expiry_date":"2024-02-15","status":"active"}'
```

### 添加线索
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --add-lead '{"source":"官网","status":"新线索","priority":"高","company":"新客户A"}'
```

### 列出所有数据
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --list
```

### 搜索竞品动态
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --competitor-news
```

### JSON格式输出
```bash
python3 ~/.qclaw/skills/pans-daily-sales-brief/scripts/brief.py --json
```

## 数据结构

数据存储在 `~/.qclaw/skills/pans-daily-sales-brief/data/pipeline.json`

```json
{
  "clients": [
    {
      "id": "client_001",
      "company": "AI Startup",
      "stage": "初步接洽",
      "next_contact": "2024-01-20",
      "notes": "对H100感兴趣",
      "created_at": "2024-01-15"
    }
  ],
  "contracts": [
    {
      "id": "contract_001",
      "client": "AI Startup",
      "amount": 500000,
      "expiry_date": "2024-02-15",
      "status": "active",
      "created_at": "2024-01-15"
    }
  ],
  "leads": [
    {
      "id": "lead_001",
      "source": "官网",
      "status": "新线索",
      "priority": "高",
      "company": "新客户A",
      "created_at": "2024-01-15"
    }
  ],
  "competitors": [
    "CoreWeave",
    "Lambda Labs",
    "RunPod",
    "Vast.ai"
  ]
}
```

## 自动化

可配合 cron 每日自动生成并发送简报。
