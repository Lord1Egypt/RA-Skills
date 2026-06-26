---
name: macro-news-signal
description: Macro News Signal is an intelligent market analysis skill that transforms real-time global news and key macro indicators into actionable investment insights.
---

# 宏观新闻信号

## 1. 概述

Macro News Signal 是一款智能市场分析工具，旨在通过自动化获取、深度解析、情感计算和多维聚合的工作流程，将碎片化的全球金融新闻与宏观经济指标转化为结构化、可操作的投资决策支持数据。

## 2.工作流程

```
新闻请求 → 来源识别 → 自动化获取 → 解析与分析 → 信号生成 → 聚合输出
```

### 2.1 第一步：来源识别

根据请求识别合适的新闻来源：

| 资产类别 | 主要来源 | 类型 |
|-------------|-----------------|------|
| 股票 | 同花顺、彭博社、CNBC | RSS |
| 固定收益 | 美联储讲话、指数、英央行 | RSS/API |
| 大宗商品 | EIA、欧佩克、金属公报 | 网页 |
| 外汇 | 央行、MNI | 网页 |
| 一般宏观 | 华尔街日报、金融时报、经济学人、联合早报 | RSS |
| 股票指数 | Yahoo Finance | API |

### 2.2 第二步：数据获取（请严格遵守下面的方案）

所有数据来源均存在 `references/news_apis.md` 中。

#### 2.2.1 RSS订阅源、指数接口 请求方式
在获取RSS订阅源、指数接口时，需要先判断是否存在curl命令时，如果存在优先使用curl进行数据获取，示例如下：
```bash
curl '地址' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
```
当不存在curl命令时，使用默认方式进行数据获取，例如web_fetch。

#### 2.2.2 股票接口 请求方式
当请求股票接口 Yahoo Finance API 时，必须使用 `scripts/format.py` 对 Yahoo Finance API 原始响应进行格式化，转化为 AI 友好的线性数据结构：

```bash
python3 scripts/format.py "<api_url>"
```

详细 API 端点和数据格式参见 `references/news_apis.md` 中的 **Yahoo Finance API** 相关说明。

### 2.3 第三步：解析与分析
该阶段利用自然语言处理 (NLP) 提取非结构化文本中的核心变量：
1. 实体提取 (NER)： 自动识别新闻中提到的特定资产（如 $NAS100$）、经济指标（如 $CPI$、$TIPS$）及关键人物或地理区域。
2. 情感极性标注：
- 鹰/鸽分析 (Hawkish/Dovish)： 针对央行沟通，量化政策偏向。
- 利好/利空 (Bullish/Bearish)： 基于金融词典计算文本情感得分 $S$。
3. 预测值比对： 若新闻涉及经济数据发布，自动对比“实际值”与“预期值”，计算超预期偏差。

### 2.4 第四步：信号生成
将解析后的分析转化为量化的投资逻辑：
- 冲击等级： 划分为 Flash (瞬时波动)、Secondary (次要影响) 或 Trend-Setting (趋势级信号)。
- 指标相关性： 宏观指标，计算当前新闻对特定资产（如黄金与 10Y TIPS 收益率背离）的映射强度。
- 逻辑校验： 自动检测是否存在“利好出尽”或“情绪过热”的背离信号。


### 2.5 第五步：聚合

按以下多维方式聚合分析结果，生成结构化报告：
- 时间窗口： 每日综述、每周深度回顾。
- 核心主题： 通货膨胀、GDP、就业市场、央行动态、地缘政治。
- 地区： 美国、中国、欧盟、新兴市场。
- 资产类别建议： 
   * 买入 (Buy)： 强利好信号且情绪合理。
   * 持有 (Hold)： 信号中性或处于数据真空期。
   * 卖出 (Sell)： 结构性利空或情感极度亢奋。

**输出格式：** 生成的报告必须严格遵循 `references/output_format.md` 中定义的模板结构，包括信号级别定义、资产信号定义和冲击强度定义。

## 3. 定义

### 3.1 信号级别定义

| 级别 | 说明 | 持续时间 |
|------|------|---------|
| **Trend-Setting** | 趋势级，影响未来数周至数月 | 长期 |
| **Sustained** | 持续级，影响未来数天至数周 | 中期 |
| **Flash** | 瞬时冲击，仅当时段有效 | 短期 |

### 3.2 资产信号定义

| 信号 | 含义 |
|------|------|
| 📈 买入 | 预计上涨，适合做多 |
| 📉 卖出 | 预计下跌，适合做空 |
| ➡️ 持有 | 预期震荡，适合观望 |

### 3.3 冲击强度定义

| 强度 | 说明 |
|------|------|
| 极高 | 重大黑天鹅，对市场有决定性影响 |
| 高 | 重要事件，能引发显著市场波动 |
| 中 | 常规事件，可能引发短期波动 |
| 低 | 次要事件，市场影响有限 |


## 4. 资源

### 4.1 references/

| 文件 | 内容 |
|------|------|
| `news_apis.md` | 新闻API文档、RSS订阅源、指数接口及 Yahoo Finance API |
| `output_format.md` | 报告输出格式模板 |

### 4.2 scripts/

| 文件 | 内容 |
|------|------|
| `format.py` | Yahoo Finance API 数据格式化脚本，将嵌套 JSON 转为扁平化结构 |