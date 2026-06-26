---
name: mx_select_stock
display_name: 妙想智能选股
description: 基于东方财富数据库的智能选股工具，支持按行情指标、财务指标等条件筛选股票。
homepage: https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA
author: 东方财富妙想团队
version: 1.0.0
env:
  - MX_APIKEY: "通过东方财富妙想平台获取的 API Key"
---

# mx_select_stock 妙想智能选股 skill

本 Skill 支持基于股票选股条件，如行情**指标、财务指标等**，筛选满足条件的股票；可查询**指定行业 / 板块内的股票、上市公司**，以及**板块指数的成分股**；同时支持**股票、上市公司、板块 / 指数推荐**等相关任务，采用此skill可避免大模型在选股时使用了过时信息。

## 配置

- **API Key**: 通过环境变量 `MX_APIKEY` 设置
- **默认输出目录**: `/root/.openclaw/workspace/mx_data/output/`（自动创建）
- **输出文件名前缀**: `mx_select_stock_`
- **输出文件**:
  - `mx_select_stock_{query}.csv` - 筛选结果 CSV 文件
  - `mx_select_stock_{query}_description.txt` - 筛选结果描述文件
