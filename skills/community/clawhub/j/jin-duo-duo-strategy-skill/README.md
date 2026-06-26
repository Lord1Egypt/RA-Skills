# 金多多股票策略分析技能包 (JinDuoDuo Strategy)

## 📈 技能概述

金多多是一个专业的股票技术分析智能体，基于6种量化交易策略，通过技术指标计算、K线形态识别和评分系统，为用户提供客观的买卖建议和风险提示。

### 核心能力

- **技术指标计算**：自动计算MA（移动平均线）、MACD、成交量分析
- **形态识别**：识别出水芙蓉、金针探底、看跌吞没等20+种K线形态
- **策略匹配**：根据评分系统匹配6种交易策略
- **风险提示**：每个策略都伴随明确的风险提示和止损建议

### 6大交易策略

| 策略 | 名称 | 类型 | 触发条件 |
|------|------|------|----------|
| 策略一 | 强势买入 | 买入 | 均线多头 + MACD金叉 + 放量突破（得分≥70） |
| 策略二 | 回踩买入 | 买入 | 上升趋势 + 回踩MA20 + 缩量止跌（得分≥60） |
| 策略三 | 突破买入 | 买入 | 底部形态突破 + 放量确认（得分≥60） |
| 策略四 | 减仓信号 | 卖出 | 顶背离 + MACD死叉 + 跌破均线（得分≥50） |
| 策略五 | 清仓信号 | 卖出 | 跌破支撑 + 空头排列 + MACD恶化（得分≥60） |
| 策略六 | 观望等待 | 观望 | 信号不明确 / 市场震荡 |

## 🚀 快速开始

### 环境要求

- Python 3.7+
- pandas >= 2.0.0
- numpy >= 1.24.0

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方式

#### 方式1：从CSV文件分析

```bash
python scripts/technical_indicators.py --input your_stock_data.csv
```

CSV文件格式要求：
```csv
日期,开盘,最高,最低,收盘,成交量
2024-01-01,10.0,10.5,9.8,10.2,1000000
2024-01-02,10.2,10.8,10.0,10.6,1200000
...
```

#### 方式2：从JSON数据快速分析

```bash
echo '{"data":[{"date":"2024-01-01","open":10.0,"high":10.5,"low":9.8,"close":10.2,"volume":1000000}]}' | \
python scripts/technical_indicators.py --input-format json
```

JSON格式要求：
```json
{
  "data": [
    {
      "date": "2024-01-01",
      "open": 10.0,
      "high": 10.5,
      "low": 9.8,
      "close": 10.2,
      "volume": 1000000
    }
  ]
}
```

#### 方式3：保存分析结果

```bash
python scripts/technical_indicators.py --input stock_data.csv --output result.json
```

## 📁 技能包结构

```
jin-duo-duo-strategy-skill/
├── SKILL.md                      # 技能主文件（技能定义）
├── SOUL.md                       # 内在人格（价值观、原则、边界）
├── IDENTITY.md                   # 外在呈现（角色、风格、标识）
├── README.md                     # 使用说明（本文件）
├── requirements.txt              # Python依赖包
├── DELIVERY.md                   # 交付物清单
├── scripts/                      # 脚本目录
│   └── technical_indicators.py # 技术指标计算脚本
└── references/                   # 参考文档目录
    └── strategy-guide.md         # 策略指南（详细策略说明）
```

## 📊 分析流程

```
1. 数据加载
   ↓
2. 技术指标计算
   ├─ MA（5/10/20/60日移动平均线）
   ├─ MACD（DIF、DEA、MACD柱）
   └─ 成交量分析（均量、量比、价量关系）
   ↓
3. 形态识别
   ├─ K线形态（出水芙蓉、金针探底等）
   ├─ 价格形态（箱体、三角形、双底等）
   └─ K线组合（红三兵、多方炮等）
   ↓
4. 策略匹配
   ├─ 评分计算
   ├─ 多策略冲突处理
   └─ 优先级排序
   ↓
5. 输出报告
   ├─ 策略类型
   ├─ 操作建议
   ├─ 关键信号
   └─ 风险提示
```

## ⚠️ 重要提示

1. **数据要求**：建议至少提供60个交易日的数据以获得准确分析
2. **仅技术分析**：本技能仅基于技术指标，不构成投资建议
3. **风险控制**：任何买入操作都应设置止损位
4. **综合判断**：建议结合基本面和市场环境综合判断
5. **持续学习**：技术分析需要经验积累，建议多复盘验证

## 📝 输出示例

```json
{
  "data_count": 60,
  "ma": {
    "MA5": [10.0, 10.2, ...],
    "MA10": [9.8, 9.9, ...],
    ...
  },
  "macd": {
    "DIF": [0.1, 0.15, ...],
    "DEA": [0.08, 0.12, ...],
    "MACD": [0.04, 0.06, ...]
  },
  "macd_signals": {
    "golden_cross": true,
    "death_cross": false,
    "top_divergence": false,
    "bottom_divergence": false
  },
  "volume": {
    "volume_ma": [1000000, 1100000, ...],
    "volume_ratio": [1.0, 1.5, ...],
    "price_up_volume_up": [false, true, ...],
    ...
  },
  "trend": {
    "trend_direction": "up",
    "bullish_arrangement": true,
    "bearish_arrangement": false,
    "is_converged": false
  }
}
```

## 🔧 自定义配置

### 调整MACD参数

编辑 `scripts/technical_indicators.py`：
```python
def calculate_macd(df: pd.DataFrame,
                   fast_period: int = 12,    # 快线周期
                   slow_period: int = 26,    # 慢线周期
                   signal_period: int = 9)   # 信号线周期
```

### 调整MA周期

编辑 `scripts/technical_indicators.py`：
```python
def calculate_ma(df: pd.DataFrame, 
                periods: List[int] = [5, 10, 20, 60]) -> Dict[str, List[float]]:
```

### 调整策略评分权重

编辑 `references/strategy-guide.md` 中的评分体系章节。

## 📚 详细文档

- **策略详细说明**：查看 `references/strategy-guide.md`
- **技术指标详解**：查看 `references/strategy-guide.md` 中的"技术指标判断标准"章节
- **K线形态识别**：查看 `references/strategy-guide.md` 中的"K线形态识别"章节

## 🤝 免责声明

本技能提供的所有分析和建议仅基于技术指标和历史数据，不构成任何投资建议。股市有风险，投资需谨慎。用户应根据自己的风险承受能力和投资目标，独立做出投资决策，并自行承担相应风险。

## 📧 技术支持

如遇到问题或建议，请检查：
1. 数据格式是否正确
2. 数据量是否充足（至少20个交易日）
3. 依赖包是否正确安装

---

**版本**：v1.0.0  
**最后更新**：2026-03-16  
**技能ID**：jin-duo-duo-strategy-skill
