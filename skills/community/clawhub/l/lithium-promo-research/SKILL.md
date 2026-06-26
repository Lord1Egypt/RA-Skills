---
name: lithium-promo-research
description: |
  锂电设备国际推广平台调研系统。针对方形电池组装线、圆柱电池组装线、软包电池组装线、切叠一体机、注液机等锂电设备产品，
  调研美国、日本、韩国、俄罗斯、欧洲等目标国家的展会推广平台、线上B2B平台、行业媒体资源。
  生成Excel格式看板报告，支持按国家/平台类型/产品线筛选分析。
  当用户需要"调研推广平台"、"找展会"、"B2B平台推荐"、"海外市场推广"、"媒体资源调研"时触发。
---

# 锂电设备国际推广平台调研 Skill

## 调研范围

### 目标国家/地区
| 编号 | 国家/地区 | 代码 |
|------|----------|------|
| 1 | 美国 | US |
| 2 | 日本 | JP |
| 3 | 韩国 | KR |
| 4 | 俄罗斯 | RU |
| 5 | 欧洲（德国/法国/意大利等） | EU |

### 平台类型
| 类型 | 说明 | 示例 |
|------|------|------|
| 展会 | 行业展会、博览会 | InterBattery, The Battery Show |
| B2B | 线上B2B交易平台 | Alibaba, EC21, Kompass |
| 媒体 | 行业媒体、杂志、新闻网站 | Batteries News, EVTech |

### 产品线（可扩展）
- 方形电池组装线
- 大小圆柱电池组装线
- 软包电池组装线
- 切叠一体机
- 注液机

> ⚠️ 产品线列表不硬编码，从 `references/product-lines.json` 动态读取，支持后期增加。

---

## 工作流程

```
[用户触发："调研XX国家推广平台"]
         ↓
[Step 1] 确定目标国家和产品线
         ↓
[Step 2] search_platforms.py   多引擎搜索平台信息
         ↓
[Step 3] parse_platforms.py    抓取详情页 + 结构化提取
         ↓
[Step 4] score_platforms.py    评分排序（影响力/匹配度/价格）
         ↓
[Step 5] generate_excel.py     生成Excel看板报告
         ↓
[Step 6] 输出报告路径 + 关键摘要
```

---

## 采集字段

每个平台记录以下字段：

| 字段 | 说明 |
|------|------|
| `platform_name` | 平台名称 |
| `platform_type` | 展会/B2B/媒体 |
| `country` | 所属国家/地区 |
| `website` | 官网链接 |
| `influence_score` | 影响力评分（1-10） |
| `audience_type` | 受众类型（电池厂/设备商/采购商） |
| `matching_products` | 匹配的产品线（多选） |
| `promo_form` | 推广形式（展位/广告/会员/新闻稿） |
| `price_range` | 价格区间（免费/低/中/高/需询价） |
| `language` | 支持语言 |
| `contact_info` | 联系方式 |
| `notes` | 备注 |
| `source_url` | 信息来源 |
| `discovered_at` | 发现时间 |

---

## 评分规则

| 维度 | 加分 | 说明 |
|------|------|------|
| 行业知名度高 | +2 | 如知名展会、头部B2B平台 |
| 受众匹配度高 | +2 | 直接面向电池制造商/设备采购商 |
| 支持多语言/英语 | +1 | 便于国际推广 |
| 有明确价格信息 | +1 | 便于预算规划 |
| 支持中国厂商参展/入驻 | +1 | 实际可操作 |
| 有锂电/新能源专区 | +2 | 垂直度高 |

**推荐等级**：S(≥7分) / A(5-6分) / B(3-4分) / C(≤2分)

---

## 搜索策略

### 按国家+类型搜索

**美国：**
- 展会：`battery show USA 2025 2026`, `lithium battery exhibition America`
- B2B：`B2B platform battery equipment USA`, `industrial equipment marketplace US`
- 媒体：`battery industry news USA`, `EV battery media America`

**日本：**
- 展会：`battery show Japan 2025`, `リチウム電池 展示会`
- B2B：`B2B バッテリー 設備`, `日本 B2B 工業設備`
- 媒体：`battery japan news`, `電池業界 メディア`

**韩国：**
- 展会：`InterBattery 2025`, `Korea battery exhibition`
- B2B：`Korea B2B platform battery`, `한국 배터리 장비 B2B`
- 媒体：`Korea battery industry news`, `배터리 산업 뉴스`

**俄罗斯：**
- 展会：`battery exhibition Russia 2025`, `выставка аккумуляторы Россия`
- B2B：`B2B platform Russia industrial equipment`
- 媒体：`battery news Russia`

**欧洲：**
- 展会：`The Battery Show Europe`, `battery exhibition Germany`
- B2B：`European B2B battery equipment marketplace`
- 媒体：`battery industry news Europe`

---

## 输出格式

### Excel看板结构

**Sheet 1: 平台总览**
| 国家 | 平台名称 | 类型 | 推荐等级 | 影响力 | 匹配产品线 | 价格 | 官网 |

**Sheet 2: 展会详情**
| 展会名称 | 国家 | 时间 | 规模 | 参展费用 | 联系方式 | 备注 |

**Sheet 3: B2B平台详情**
| 平台名称 | 国家 | 入驻费用 | 佣金 | 受众 | 语言支持 | 链接 |

**Sheet 4: 媒体资源**
| 媒体名称 | 国家 | 类型 | 广告价格 | 发行量/流量 | 投稿方式 | 链接 |

**Sheet 5: 按产品线推荐**
| 产品线 | 推荐平台 | 类型 | 国家 | 推荐理由 |

---

## 使用方式

### 命令行调用
```powershell
# 完整调研流程
python scripts/main.py --country KR --type exhibition

# 跳过搜索，直接用现有数据生成报告
python scripts/main.py --skip-search --output my_report.xlsx

# 指定产品线
python scripts/main.py --country US --type b2b --product "方形电池组装线" "圆柱电池组装线"
```

### 参数说明
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|-------|
| --country | -c | 目标国家(US/JP/KR/RU/EU/ALL) | ALL |
| --type | -t | 平台类型(exhibition/b2b/media/all) | all |
| --product | -p | 产品线(多选) | 全部 |
| --output | -o | 输出文件名 | promo_report_YYYYMMDD.xlsx |
| --skip-search | - | 跳过搜索，直接用现有数据 | false |

### 手动触发
```
"帮我调研韩国锂电设备推广平台"
"美国有哪些电池展会"
"生成推广平台调研报告"
"调研日本B2B平台"
```

---

## 文件结构

```
lithium-promo-research/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── main.py                    # 主入口CLI
│   ├── search_platforms.py           # 多引擎搜索
│   ├── parse_platforms.py            # 详情抓取+结构化
│   ├── score_platforms.py            # 评分排序
│   └── generate_excel.py             # 生成Excel看板
├── references/
│   ├── product-lines.json            # 产品线配置（可扩展）
│   ├── country-guides/               # 各国详细指南
│   │   ├── us.md
│   │   ├── jp.md
│   │   ├── kr.md
│   │   ├── ru.md
│   │   └── eu.md
│   └── search-templates.md           # 搜索模板库
├── data/
│   ├── platforms_raw_YYYYMMDD.json   # 原始搜索结果
│   └── reports/
│       └── promo_report_YYYYMMDD.xlsx # Excel看板报告
└── assets/
    └── (可选) Excel模板文件
```

---

## 状态输出

调研完成后输出：
- 新发现平台数量
- 各国家/类型分布
- 推荐等级分布（S/A/B/C 各多少）
- Excel报告文件路径
- 关键推荐（Top 5 平台）
