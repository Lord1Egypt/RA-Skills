# 持仓诊断与分析 (Holdings Analysis)

## 简介

持仓实时诊断工具。读取持仓列表，调用腾讯API获取实时行情，结合技术指标计算买入评分（M/A/R/V四维）和卖出评分，给出PASS/FAIL状态和操作信号。

---

## 核心文件

| 文件 | 用途 |
|------|------|
| `_holdings_std.py` | 持仓数据（成本价、买入日期） |
| `check_holdings_v4.py` | 主脚本：买入评分 + M/A/R/V + 卖出评分 + PASS/FAIL |
| `analyze_holdings.py` | v1版持仓分析 |
| `analyze_holdings_v2.py` | v2版持仓分析 |
| `check_holdings_detail.py` | 持仓详情（含趋势追踪） |
| `check_holdings_trend.py` | 持仓趋势追踪 |
| `run_holdings.py` | 快速运行入口 |

---

## 使用方法

```bash
# 标准持仓诊断
python check_holdings_v4.py

# 持仓趋势追踪
python check_holdings_trend.py
```

---

## 评分体系

### 买入评分（满分100）
- **PASS** 阈值：≥55分，进入趋势合格池
- **FAIL** 阈值：<55分，不符合趋势选股标准

### 卖出评分（满分100）
- 评分越高代表风险越大
- 参考阈值：≥25分考虑分批止盈，≥40分强烈建议离场

### M/A/R/V 四维
- **M**：动能（MACD方向）
- **A**：结构（均线排列）
- **R**：RSI强弱
- **V**：量价配合

---

## 输出格式

```
代码 名称   评分  M/A/R/V   卖出评分  状态  盈亏%
000682 东方电子  59  21/20/18/0  20  PASS  -1.1%
```

---

## 持仓数据维护

编辑 `_holdings_std.py` 中的 `HOLDINGS` 列表添加新持仓：
```python
HOLDINGS = [
    {"code": "000682", "buy_price": 13.20, "buy_date": "2026-03-30"},
    {"code": "300529", "buy_price": 18.60, "buy_date": "2026-04-22"},
]
```

---

## 免责声明

本系统仅供学习研究使用，不构成任何投资建议。
