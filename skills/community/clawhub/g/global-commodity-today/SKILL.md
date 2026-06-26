---
name: global-commodity-today
description: 全球大宗商品行情简报工具，支持查询伦敦金、伦敦银、伦敦铜、纽约铂、布伦特原油的当前价格和当日涨跌幅，生成简洁的行情简报。基于akshare获取实时数据。
---

# Global Commodity Today Skill

全球大宗商品行情简报工具，快速获取贵金属与原油的实时价格与涨跌幅。

## When to Use

当用户请求以下操作时调用此skill：
- 查询伦敦金（XAU）、伦敦银（XAG）、伦敦铜、纽约铂的当前价格
- 查询布伦特原油的当前价格
- 获取贵金属/原油的当日涨跌幅
- 生成大宗商品行情简报
- 了解当日贵金属和原油市场概况

## Prerequisites

### Python环境要求
```bash
pip install akshare pandas
```

### 依赖检查
在执行前，先检查akshare是否已安装：
```bash
python -c "import akshare; print(akshare.__version__)"
```

如果未安装，提示用户安装：
```bash
pip install akshare pandas
```

## Supported Commodities

| 品种 | 代码 | 单位 | 说明 |
|------|------|------|------|
| 伦敦金 | XAU | 美元/盎司 | London Gold Spot |
| 伦敦银 | XAG | 美元/盎司 | London Silver Spot |
| 伦敦铜 | CAD | 美元/吨 | LME Copper |
| 纽约铂 | PLT | 美元/盎司 | NYMEX Platinum |
| 布伦特原油 | OIL | 美元/桶 | Brent Crude Oil |

---

## Workflow 1: Quick Briefing (快速行情简报)

用户请求查看大宗商品行情或简报时使用。这是最常用的工作流程。

### Step 1: Fetch Commodity Data

运行数据获取脚本，获取所有品种的实时价格和涨跌幅（默认输出文本简报）：

```bash
python scripts/precious_metals_oil_fetcher.py --mode briefing
```

**参数说明：**
- `--mode`: 运行模式，`briefing` 为简报模式（获取所有品种）

### Step 2: Present Briefing Report

脚本默认直接输出结构化的文本简报（Markdown格式），可直接呈现给用户。

**简报格式示例：**

#### 📊 大宗商品行情简报

> 数据时间：2025-01-25 15:30:00

| 品种 | 最新价 | 涨跌幅 | 涨跌额 | 今开 | 最高 | 最低 |
|------|--------|--------|--------|------|------|------|
| 🟡 伦敦金 | 2,758.30 | +0.85% | +23.20 | 2,735.10 | 2,762.50 | 2,730.00 |
| ⚪ 伦敦银 | 31.25 | +1.20% | +0.37 | 30.88 | 31.40 | 30.75 |
| 🟤 伦敦铜 | 9,325.00 | -0.45% | -42.00 | 9,367.00 | 9,380.00 | 9,300.00 |
| 🔘 纽约铂 | 965.50 | +0.30% | +2.90 | 962.60 | 968.00 | 960.00 |
| 🛢️ 布伦特原油 | 78.65 | -1.10% | -0.87 | 79.52 | 79.80 | 78.20 |

**市场摘要：**
- 贵金属板块整体偏强，伦敦金续创新高
- 原油受需求担忧影响小幅回落
- 伦敦铜受宏观情绪影响微跌

---

## Workflow 2: Single Commodity Query (单品种查询)

用户只关注某一个品种时使用。

### Step 1: Fetch Single Commodity

```bash
python scripts/precious_metals_oil_fetcher.py --mode single --commodity gold
```

**`--commodity` 可选值：**
- `gold` - 伦敦金
- `silver` - 伦敦银
- `copper` - 伦敦铜
- `platinum` - 纽约铂
- `oil` - 布伦特原油

### Step 2: Present Result

以单品种详情方式展示，包含当前价格、涨跌幅、日内高低点等。

---

---

## Error Handling

### 网络错误
如果数据获取失败，提示用户：
1. 检查网络连接
2. 稍后重试（可能是接口限流）
3. 部分品种可能因交易时间未到而无数据

### 非交易时间
- 贵金属和原油均为全球交易品种，几乎24小时可获取行情
- 周末和节假日可能只能获取上一交易日的收盘数据
- 脚本会自动标注数据时间，方便用户判断时效性

### 数据异常
- 如果某个品种获取失败，不影响其他品种的显示
- 失败品种会标注"数据获取失败"

---

## Best Practices

1. **数据时效性**：显示的价格为最近可获取的行情数据，需注意数据时间
2. **汇率换算**：所有价格均以美元计价，如需人民币价格可提示用户参考当日汇率
3. **投资建议**：所有数据仅供参考，不构成投资建议
4. **使用频率**：建议间隔至少1分钟以上再次获取，避免接口限流

## Important Notes

- 本工具仅提供公开市场数据查询功能
- 数据来源为akshare聚合的公开行情接口
- 不同交易所的报价可能略有差异，以实际交易平台为准
- 涨跌幅基于前一交易日收盘价计算
