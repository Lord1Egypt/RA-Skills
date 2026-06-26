# Kelly Formula Crypto - 凯利公式仓位管理器

<div align="center">

**AI加密交易的仓位管理工具**

版本: **1.0.0**
定价: **0.01 USDC** (x402支付)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

</div>

---

## 🎯 简介

基于凯利公式(Kelly Criterion)的加密货币仓位计算工具，帮助交易者用数学纪律替代情绪化决策。

**核心功能**：
- ✅ 凯利公式仓位计算
- ✅ 分数凯利建议（½ / ¼）
- ✅ 多策略仓位分配
- ✅ 杠杆安全边际计算
- ✅ x402微支付支持

---

## 💰 价格

**0.01 USDC** - 通过x402协议支付

```bash
# 支付示例
curl -X POST https://api.x402.dev/pay \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0x24b288c98421d7b447c2d6a6442538d01c5fce22",
    "amount": "0.01",
    "currency": "USDC",
    "memo": "kelly-formula-crypto"
  }'
```

---

## 📖 核心公式

### 完整版
```
f* = (bp - q) / b
```
- `p` = 胜率
- `b` = 盈亏比
- `q` = 1 - p

### 简化版（对称盈亏）
```
f* ≈ 2p - 1
```
> 记忆法：胜率高出50%的部分×2 = 建议仓位

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/jinboh68-prog/kelly-formula-crypto.git
cd kelly-formula-crypto
pip install -r requirements.txt
```

### 使用

```bash
# 基本用法
python scripts/kelly_calculator.py -p 0.55 -w 5 -l 3

# 使用½凯利
python scripts/kelly_calculator.py -p 0.60 -w 5 -l 3 -f 0.5

# 杠杆检查
python scripts/kelly_calculator.py -p 0.55 -w 5 -l 3 --leverage 5 --liquidation 10 --stop-loss 3

# JSON输出
python scripts/kelly_calculator.py -p 0.70 -w 2 -l 1 --json
```

### 示例输出

```
📊 Kelly Formula 计算结果
========================================
胜率: 55% | 盈亏比: 1.67

🧮 仓位建议:
  全凯利: 28.0%
  ½凯利:  14.0%
  ¼凯利:  7.0%

✅ 推荐仓位: 14.0%
```

---

## 📊 对称速查表

| 胜率 | 全凯利 | ½凯利 | ¼凯利 |
|:----:|:------:|:-----:|:-----:|
| 52% | 4%     | 2%    | 1%    |
| 55% | 10%    | 5%    | 2.5%  |
| 60% | 20%    | 10%   | 5%    |
| 65% | 30%    | 15%   | 7.5%  |
| 70% | 40%    | 20%   | 10%   |
| 75% | 50%    | 25%   | 12.5% |

---

## ⚠️ 8条铁律

1. **默认分数凯利**：先用½，带杠杆/不稳用¼
2. **摩擦全进账**：费率、滑点、资金费、Gas全部计入
3. **滚动估参**：月/季更新，重大事件临时降档
4. **三道闸门**：单笔、单日、单策略回撤硬阈值
5. **净敞口上限**：相关性高时顶层总仓要有硬帽
6. **极端日流程**：深度骤降/维护 → 切防守模板
7. **小样本慎重**：<200笔做保守收缩
8. **先截尾再放大**：先证明能控制最大亏损，再考虑放大

---

## 🔧 API

```python
from kelly_calculator import kelly_position, calculate_trade

# 基础计算
position = kelly_position(p=0.55, b=1.67, fraction=0.5)
print(f"建议仓位: {position*100}%")

# 完整计算
result = calculate_trade(
    p=0.60,
    win_pct=5,
    loss_pct=3,
    fraction=0.5,
    leverage=3,
    liquidation_pct=20,
    stop_loss_pct=5
)
print(result)
```

---

## 📚 案例

### 案例1：BTC短线趋势
- 胜率 55%，盈亏比 5%/3%
- 净优势 = 0.55×5 - 0.45×3 = 1.4%
- 建议仓位 = 1.4 ÷ 5 = 28%
- **执行½ = 14%**

### 案例2：ETH资金费套利
- 胜率 70%，盈亏比 2%/1%
- 净优势 = 1.4 - 0.3 = 1.1%
- 建议仓位 = 55%
- **执行¼-½ = 14-27%**

### 案例3：Meme热点
- 表面：胜率58%，盈亏比7%/5%
- 但1/6亏损是-25%插针
- 真实亏损 = 5/6×5% + 1/6×25% = 8.3%
- 新净优势 = 4.06 - 3.49 = 0.57%
- **建议仓位 ≈ 8% → 执行2-4%**

---

## ⚡️ 风险提示

- 凯利公式假设你能准确估计胜率和盈亏比
- 现实中有"肥尾"，历史数据不代表未来
- 分数凯利比全凯利更安全
- 杠杆交易有强平风险，必须先算安全边际

---

## 📖 参考资料

- Kelly, J.L. (1956) "A New Interpretation of Information Rate"
- Edward Thorp "Beat the Dealer", "Advances in Large Scale Actors"
- 原始文章: https://x.com/KKaWSB/status/1968453490084299020

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 相关链接

- GitHub: https://github.com/jinboh68-prog/kelly-formula-crypto
- 作者: @samhuang2025
- Telegram: @samhuang2025
