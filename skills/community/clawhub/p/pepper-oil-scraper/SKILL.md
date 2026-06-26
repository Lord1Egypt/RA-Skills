---
name: pepper-oil-scraper
description: >
  爬取花椒油、藤椒油产业链相关数据的专用技能。覆盖市场规模、原料价格、企业财报、
  进出口、行业报告、竞争格局等多维度数据源，内置 20+ 重点网站的爬虫适配器。
  当用户需要采集花椒/藤椒/调味油/Sichuan Pepper Oil 相关产业数据时触发此技能。
  即使用户只说"爬数据""抓取报告""采集价格"，只要上下文涉及花椒、藤椒、调味品
  产业链，就应该使用此技能。也可作为农产品产业链爬虫的通用模板。
metadata:
  openclaw:
    emoji: "🌶️"
    requires:
      bins:
        - python3
        - pip
      env: []
    install:
      - id: pip-deps
        kind: node
        label: "Install Python dependencies"
---

# 花椒油/藤椒油产业数据爬虫技能

## 概述

本技能提供一套完整的 Python 爬虫工具集，用于从 20+ 个重点数据源采集花椒/藤椒产业链数据。

## 快速开始

```bash
# 1. 安装依赖
pip install requests beautifulsoup4 lxml pandas openpyxl aiohttp fake-useragent --break-system-packages

# 2. 运行采集
python scripts/main_crawler.py --all --output /home/claude/pepper_data/

# 3. 按类别采集
python scripts/main_crawler.py --category price    # 原料价格
python scripts/main_crawler.py --category market   # 行业报告
python scripts/main_crawler.py --category company  # 企业数据
python scripts/main_crawler.py --category gov      # 政府数据
python scripts/main_crawler.py --category media    # 媒体报道
python scripts/main_crawler.py --category global   # 全球市场

# 4. 单站点采集
python scripts/main_crawler.py --site cnhnb        # 惠农网价格
python scripts/main_crawler.py --site cnfin_index  # 新华花椒指数

# 5. 导出报告
python scripts/export_report.py --input /home/claude/pepper_data/ --output /mnt/user-data/outputs/花椒产业数据.xlsx
```

---

## 重点数据源（26 个站点）

### A. 原料价格与供需（5 站）

| 站点 | 域名 | adapter_id | 采集内容 |
|------|------|------------|---------|
| 惠农网 | cnhnb.com | `cnhnb` | 花椒/藤椒实时批发价、历史价格走势 |
| 一亩田 | ymt.com | `ymt` | 产地收购价、供应商报价 |
| 新华花椒价格指数 | indices.cnfin.com | `cnfin_index` | 武都花椒价格指数（日/周/月） |
| 花椒大数据网 | 860938.cn | `huajiao_bigdata` | 各产区价格、种植面积、产量 |
| 中国花椒网 | huajiao.cn | `huajiao_cn` | 花椒行情、产区动态 |

### B. 行业研究报告（6 站）

| 站点 | 域名 | adapter_id | 采集内容 |
|------|------|------------|---------|
| 观研天下 | chinabaogao.com | `chinabaogao` | 花椒油/藤椒油行业报告摘要 |
| 中商产业研究院 | askci.com | `askci` | 市场规模预测、竞争格局 |
| 智研咨询 | chyxx.com | `chyxx` | 行业深度报告、产量数据 |
| 前瞻产业研究院 | qianzhan.com | `qianzhan` | 行业趋势、市场前景 |
| 中研网 | chinairn.com | `chinairn` | 花椒油市场规模、增长率 |
| 共研网 | gonyn.com | `gonyn` | 产业链分析、市场预测 |

### C. 企业与财报（4 站）

| 站点 | 域名 | adapter_id | 采集内容 |
|------|------|------------|---------|
| 巨潮资讯网 | cninfo.com.cn | `cninfo` | 招股书、年报（幺麻子/天味/颐海等） |
| 东方财富 | eastmoney.com | `eastmoney` | 财务数据、研报 |
| 新浪财经 | finance.sina.com.cn | `sina_finance` | 企业新闻、财报解读 |
| 导油网 | oilcn.com | `oilcn` | 食用油行业动态 |

### D. 政府与标准（4 站）

| 站点 | 域名 | adapter_id | 采集内容 |
|------|------|------------|---------|
| 国家林草局 | forestry.gov.cn | `forestry` | 花椒种植面积、产量、政策 |
| 农业农村部 | moa.gov.cn | `moa` | 农产品市场信息 |
| 海关总署 | customs.gov.cn | `customs` | 进出口数据 (HS:0910991000) |
| 标准全文公开系统 | openstd.samr.gov.cn | `samr_std` | 花椒油国标/行标 |

### E. 财经媒体（4 站）

| 站点 | 域名 | adapter_id | 采集内容 |
|------|------|------------|---------|
| 36氪 | 36kr.com | `kr36` | 企业分析、融资动态 |
| 界面新闻 | jiemian.com | `jiemian` | 行业深度报道 |
| CBNData | cbndata.com | `cbndata` | 消费数据、企业分析 |
| 央广网 | cnr.cn | `cnr` | 花椒产业研究报告 |

### F. 全球市场（3 站）

| 站点 | 域名 | adapter_id | 采集内容 |
|------|------|------------|---------|
| Business Research Insights | businessresearchinsights.com | `bri` | 全球 Prickly Ash Oil 市场 |
| Verified Market Reports | verifiedmarketreports.com | `vmr` | 全球花椒油预测 |
| WiseGuy Reports | wiseguyreports.com | `wiseguy` | 四川风味全球市场 |

---

## 架构

```
pepper-oil-scraper/
├── SKILL.md
├── config/
│   └── targets.json             # 全部站点配置
├── scripts/
│   ├── main_crawler.py          # 主调度入口
│   ├── base_scraper.py          # 基类：反爬、重试、限速
│   ├── adapters/
│   │   ├── __init__.py          # 适配器注册表
│   │   ├── price_adapters.py    # A 组：价格站点
│   │   ├── report_adapters.py   # B 组：报告站点
│   │   ├── company_adapters.py  # C 组：企业站点
│   │   ├── gov_adapters.py      # D 组：政府站点
│   │   ├── media_adapters.py    # E 组：媒体站点
│   │   └── global_adapters.py   # F 组：全球站点
│   ├── data_cleaner.py          # 数据清洗与标准化
│   └── export_report.py         # 导出 Excel 报告
├── references/
│   └── anti_crawl_guide.md      # 反爬策略参考
└── templates/
    └── report_template.md       # 报告输出模板
```

## 反爬策略

- 请求间隔 2-5 秒随机延迟（configurable per site）
- fake-useragent 随机 UA
- 带 Referer 头模拟正常浏览
- 403/429 指数退避（2s → 4s → 8s → ... → 60s max）
- 支持代理池配置
- 对 JS 重站点说明使用 playwright（需用户手动安装）

## 数据标准化

所有输出统一单位：价格→元/公斤，面积→万亩，产量→万吨，金额→亿元。
每条数据必须携带 source_url、crawl_time、original_text 字段。
