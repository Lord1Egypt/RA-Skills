# 宏观经济资讯 (Macro Information)

基于 FEEDAX API 的宏观经济资讯与舆情监测技能，提供全面的宏观经济数据查询能力。

## 📊 功能概述

支持查询国内外宏观经济相关新闻资讯，包括：
- **经济数据**: GDP、CPI、PPI、PMI、失业率等
- **货币政策**: 美联储、人民银行、降准降息等
- **财政政策**: 财政刺激、基建投资、减税政策等
- **国际贸易**: 中美贸易、关税政策、进出口数据等
- **金融市场**: 股市、债市、汇率、房地产等

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
macro-information/
├── SKILL.md                          # 技能说明文档
├── README.md                         # 本文件
└── scripts/
    ├── query_macro_information.py      # 查询脚本
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
python scripts/query_macro_information.py --api-key "your-api-key" --keyword "GDP"
```

**方式 2: 环境变量**
```bash
export FEEDAX_API_KEY="your-api-key"
python scripts/query_macro_information.py --keyword "GDP"
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
# 查询国内宏观资讯
python scripts/query_macro_information.py --keyword "GDP" --macro-type 国内宏观 --days 7

# 查询国际宏观资讯
python scripts/query_macro_information.py --keyword "美联储" --macro-type 国际宏观 --days 14

# 查询负面宏观资讯
python scripts/query_macro_information.py --keyword "通胀" --sentiments 负面 --days 30

# 按热度排序
python scripts/query_macro_information.py --keyword "加息" --macro-type 国际宏观 --sort-by heat_scores
```

---

## 参数说明

### 必填参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--keyword` | `-k` | 搜索关键词 |

### 宏观类型筛选

| 参数 | 简写 | 可选值 |
|------|------|--------|
| `--macro-type` | `-m` | 国内宏观 / 国际宏观 |

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

- **文件名**: `macro_information_<时间戳>.csv`
- **字段**: 发布时间、标题、来源、情感倾向、宏观类型、事件标签、涉及地区、重要程度、热度得分、浏览数、转发数、URL

### MD 说明文件

- **文件名**: `macro_information_<时间戳>.md`
- **内容**: 查询统计、宏观类型分布、情感分布、事件标签、涉及地区等

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
| `macroEconomyResult` | 宏观类型（国内宏观/国际宏观） |
| `macroTag` | 宏观事件标签 |
| `areaResult` | 涉及地区 |
| `newsImportanceLevel` | 重要程度（高/中/低） |
| `heatScores` | 资讯热度得分 |
| `viewNum` | 浏览数 |
| `forwardedNum` | 转发数 |

---

## 宏观类型分类

| 类型 | 说明 |
|------|------|
| **国内宏观** | 中国宏观经济相关政策、数据、事件 |
| **国际宏观** | 全球宏观经济、主要央行政策、国际经济事件 |

---

## 常见事件标签

- **货币政策**: 降准、降息、加息、缩表、扩表
- **财政政策**: 财政刺激、基建投资、减税降费
- **经济数据**: GDP、CPI、PPI、PMI、失业率
- **国际贸易**: 关税、贸易摩擦、进出口
- **金融市场**: 股市、债市、汇率、房地产
- **央行政策**: 美联储、人民银行、欧央行、日银

---

## 示例输出

```
共找到 20 条资讯:

================================================================================
1. [2026-04-02 14:30] 🟢 正面 🇨🇳 国内宏观
   标题：一季度 GDP 同比增长 5.2%，经济开局良好
   来源：财经日报 | 热度：85.3
   事件标签：经济数据
   涉及地区：全国
--------------------------------------------------------------------------------
2. [2026-04-02 12:15] 🟡 中性 🌍 国际宏观
   标题：美联储宣布维持利率不变
   来源：新浪财经 | 热度：92.1
   事件标签：货币政策
   涉及地区：美国
--------------------------------------------------------------------------------
```

---

## 示例对话

**用户**: 搜索最近 7 天关于美联储加息的国际宏观新闻，按热度排序

**执行命令**:
```bash
python scripts/query_macro_information.py \
    --keyword "加息" \
    --macro-type 国际宏观 \
    --days 7 \
    --sort-by heat_scores
```

---

## 注意事项

1. **时间参数**: 使用 Unix 时间戳（毫秒），脚本会自动计算
2. **页码**: 从 0 开始计数
3. **情感倾向**: 正面、负面、中性，不传表示全部
4. **宏观类型**: 国内宏观、国际宏观，不传表示全部
5. **API Key**: 必须提供，支持三种配置方式
6. **输出文件**: 默认生成 CSV 和 MD 文件，可使用 `--no-output` 禁用

---

## 接口信息

- **接口地址**: `221.6.15.90:18011`
- **接口 URI**: `/data-service/v1/news/macro/external/query`
- **请求方式**: `POST`
- **Content-Type**: `application/json; charset=UTF-8`

---

**数据来源**: FEEDAX 宏观资讯监测平台  
**数据范围**: 新闻、微信公众号、微博等多种信源

---

*最后更新：2026-04-02*
