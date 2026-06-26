# 行业资讯 (Industry Information)

基于 FEEDAX API 的行业资讯与舆情监测技能，提供全面的行业数据查询能力。

## 📊 功能概述

支持查询特定行业的新闻资讯和舆情动态，包括：
- **行业趋势**: 房地产、人工智能、新能源、半导体等
- **舆情监测**: 行业负面新闻、风险预警、口碑分析
- **行业对比**: 多行业舆情对比、投资价值分析
- **政策影响**: 产业政策效果评估、政策影响分析

## ⚠️ 前置条件：配置 API Key

**使用本技能前，必须先配置 API Key。**

### API Key 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| GE1003 | 未配置 API Key | 前往 https://www.feedax.cn 申请 |
| GE1004 | API Key 已失效 | 检查 API Key 有效性，或重新申请 |
| GE1005 | API Key 已过期 | 前往 https://www.feedax.cn 重新申请 |
| GE1006 | API Key 无效 | 前往 https://www.feedax.cn 重新申请 |
| GE1007 | 账户余额不足 | 前往 https://www.feedax.cn 充值 |

### 服务错误处理

| HTTP 状态码 | 错误提示 |
|------------|----------|
| 400 | 请求参数错误，请检查输入 |
| 401/403 | API Key 可能无效或已过期 |
| 429 | 请求过于频繁，请稍后再试 |
| 500 | 服务器内部错误 |
| 502 | 服务暂时不可用，请稍后再试 |
| 503 | 服务维护中，请稍后再试 |
| 504 | 网关超时，请稍后再试 |

---

## 文件结构

```
industry-information/
├── SKILL.md                          # 技能说明文档
├── README.md                         # 本文件
└── scripts/
    ├── query_industry_information.py   # 查询脚本
    └── config.json                   # API Key 配置文件（可选）
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key（三选一）

**方式 1: 命令行参数（推荐）**
```bash
python scripts/query_industry_information.py --api-key "your-api-key" --keyword "房地产"
```

**方式 2: 环境变量**
```bash
export FEEDAX_API_KEY="your-api-key"
python scripts/query_industry_information.py --keyword "房地产"
```

**方式 3: 配置文件**
在 `scripts/` 目录创建 `config.json` 文件：
```json
{
  "api_key": "your-api-key"
}
```

### 3. 基本用法

```bash
# 查询负面行业资讯
python scripts/query_industry_information.py --keyword "房地产" --sentiments 负面 --days 7

# 查询特定行业
python scripts/query_industry_information.py --keyword "人工智能" --days 14

# 查询新能源行业
python scripts/query_industry_information.py --keyword "新能源" --sentiments 正面 --days 30

# 按热度排序
python scripts/query_industry_information.py --keyword "半导体" --sort-by heat_scores
```

---

## 参数说明

### 必填参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--keyword` | `-k` | 搜索关键词（行业名称） |

### 情感筛选

| 参数 | 简写 | 可选值 |
|------|------|--------|
| `--sentiments` | `-s` | 正面 / 负面 / 中性（可多选） |

### 分页与排序

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--days` | `-d` | 7 | 查询天数 |
| `--page` | `-p` | 0 | 页码（从 0 开始） |
| `--size` | `-n` | 20 | 每页数量 |
| `--sort-by` | | `publish_date` | 排序字段：publish_date / heat_scores |
| `--sort-type` | | `DESC` | 排序方式：ASC / DESC |

### 输出控制

| 参数 | 简写 | 说明 |
|------|------|------|
| `--verbose` | `-v` | 显示详细内容（摘要） |
| `--output-dir` | | 输出目录（默认当前目录） |
| `--no-output` | | 不生成输出文件，仅显示结果 |
| `--api-key` | | FEEDAX API Key |

---

## 输出文件

### CSV 文件

- **文件名**: `industry_information_<时间戳>.csv`
- **字段**: 发布时间、标题、摘要、内容、来源、证监会行业、申万行业、行业标签、重要程度、热度得分、浏览数、转发数、URL

### MD 说明文件

- **文件名**: `industry_information_<时间戳>.md`
- **内容**: 查询统计、证监会行业分布、申万行业分布、情感分布、行业标签、涉及地区等

---

## 数据字段说明

| 字段 | 说明 |
|------|------|
| `title` | 新闻标题 |
| `content` | 新闻正文 |
| `summary` | 摘要 |
| `source` | 新闻来源 |
| `url` | 原文链接 |
| `publishDate` | 发布时间（13 位时间戳） |
| `sentiment` | 情感倾向（正面/负面/中性） |
| `industryAspectSentiment` | 行业正负面 |
| `csrcIndustryVos` | 证监会行业结果 |
| `industrySwResultVos` | 申万行业结果 |
| `industryTags` | 行业标签 |
| `newsImportanceLevel` | 重要程度（高/中/低） |
| `heatScores` | 资讯热度得分 |
| `viewNum` | 浏览数 |
| `forwardedNum` | 转发数 |

---

## 行业分类

### 证监会行业分类

| 行业大类 | 行业子类示例 |
|---------|-------------|
| 农、林、牧、渔业 | 农业、林业、畜牧业、渔业 |
| 采矿业 | 煤炭开采、石油开采 |
| 制造业 | 食品制造、医药制造、汽车制造 |
| 信息传输、软件和信息技术服务业 | 电信、互联网、软件服务 |
| 金融业 | 银行、证券、保险 |
| 房地产业 | 房地产开发、物业管理 |
| ... | ... |

### 申万行业分类（28 个一级行业）

农林牧渔、食品饮料、纺织服装、轻工制造、医药生物、化工、钢铁、有色金属、电子、计算机、传媒、通信、电气设备、机械设备、国防军工、汽车、家用电器、建筑材料、建筑装饰、房地产、商业贸易、休闲服务、银行、非银金融、综合、交通运输、公用事业、采掘

---

## 常见行业标签

- **政策类**: 产业政策、监管政策、税收政策、补贴政策
- **市场类**: 市场需求、市场竞争、市场价格
- **技术类**: 技术创新、技术突破、数字化转型
- **资本类**: 投融资、并购重组、IPO
- **经营类**: 业绩增长、产能扩张、成本控制
- **风险类**: 行业风险、经营风险、政策风险

---

## 示例输出

```
共找到 20 条资讯:

================================================================================
1. [2026-04-02 14:30] 🟢 正面
   标题：人工智能行业迎来新的发展机遇
   来源：新浪财经 | 热度：85.3
   证监会行业：信息传输、软件和信息技术服务业
   申万行业：计算机
   行业标签：技术创新
--------------------------------------------------------------------------------
```

---

## 示例对话

**用户**: 搜索最近 7 天人工智能行业的正面新闻，按热度排序

**执行命令**:
```bash
python scripts/query_industry_information.py \
    --keyword "人工智能" \
    --sentiments 正面 \
    --days 7 \
    --sort-by heat_scores
```

---

## 注意事项

1. **时间参数**: 使用 Unix 时间戳（毫秒），脚本会自动计算
2. **页码**: 从 0 开始计数
3. **情感倾向**: 正面、负面、中性，不传表示全部
4. **行业分类**: 支持证监会行业和申万行业分类
5. **API Key**: 必须提供，支持三种配置方式
6. **输出文件**: 默认生成 CSV 和 MD 文件，可使用 `--no-output` 禁用

---

## 接口信息

- **接口地址**: `221.6.15.90:18011`
- **接口 URI**: `/data-service/v1/news/industry/external/query`
- **请求方式**: `POST`
- **Content-Type**: `application/json; charset=UTF-8`

---

**数据来源**: FEEDAX 行业资讯监测平台  
**数据范围**: 新闻、微信公众号、微博等多种信源

---

*最后更新：2026-04-02*
