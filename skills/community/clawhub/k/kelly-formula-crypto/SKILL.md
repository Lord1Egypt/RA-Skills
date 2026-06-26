---
name: kelly-formula-crypto
description: 🎯 Kelly Formula 仓位管理器 - 凯利公式加密货币仓位计算工具
author: Rich
version: 1.0.0
tags:
  - kelly-formula
  - crypto
  - trading
  - position-sizing
  - risk-management
  - 仓位管理
openclaw_version: ">=2025.1.0"
# x402收费配置
endpoint: "https://kelly-formula-crypto.vercel.app/api/calculate"
auth_type: "x402"
price: "0.01"
currency: "USDC"
chain: "Base"
wallet: "0x24b288c98421d7b447c2d6a6442538d01c5fce22"
capabilities:
  - api_call
---

# Kelly Formula 仓位管理器

**定价**: 0.01 USDC (x402支付)
**标签**: crypto, trading, kelly-formula, position-sizing, risk-management
**作者**: Rich (@samhuang2025)

---

## 简介

基于凯利公式的加密货币仓位计算工具，帮助交易者用数学纪律替代情绪化决策。

**核心功能**：
- ✅ 凯利公式仓位计算
- ✅ 分数凯利建议（½ / ¼）
- ✅ 多策略仓位分配
- ✅ 杠杆安全边际计算

---

## x402 支付

本skill支持x402微支付协议。调用时自动发起0.01 USDC支付请求。

```bash
# x402支付示例
curl -X POST https://api.x402.dev/pay \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0x24b288c98421d7b447c2d6a6442538d01c5fce22",
    "amount": "0.01",
    "currency": "USDC",
    "memo": "kelly-formula-skill"
  }'
```

---

## 核心公式

### 完整版
```
f* = (bp - q) / b
```
- p = 胜率
- b = 盈亏比
- q = 1 - p

### 简化版（对称盈亏）
```
f* ≈ 2p - 1
```
记忆法：胜率高出50%的部分×2 = 建议仓位

---

## 使用方法

### 1. 基本仓位计算

**输入**：
- 胜率 p (0-1)
- 盈亏比 b (如 2.0 表示赚2块亏1块)

**输出**：
- 全凯利仓位
- ½凯利仓位（推荐）
- ¼凯利仓位（保守/杠杆）

```python
def kelly_position(p, b, fraction=0.5):
    if p <= 0.5:
        return 0  # 无优势，不做
    f_star = (p * b - (1 - p)) / b
    if f_star < 0:
        return 0
    return f_star * fraction
```

### 2. 对称速查表

| 胜率 | 全凯利 | ½凯利 | ¼凯利 |
|------|--------|-------|-------|
| 52%  | 4%     | 2%    | 1%    |
| 55%  | 10%    | 5%    | 2.5%  |
| 60%  | 20%    | 10%   | 5%    |
| 65%  | 30%    | 15%   | 7.5%  |
| 70%  | 40%    | 20%   | 10%   |
| 75%  | 50%    | 25%   | 12.5% |

### 3. 多策略仓位分配

**原则**：相关性>0.7时，合并仓位打7折

```python
def adjusted_position(positions, correlation, discount=0.7):
    total = sum(positions)
    if correlation > 0.7:
        return total * discount
    return total
```

### 4. 杠杆安全边际

```python
def leverage_safety(liquidation_distance, stop_loss):
    safety_factor = liquidation_distance / stop_loss
    if safety_factor < 2:
        return "不安全，建议降杠杆"
    return "安全"
```

---

## 实战案例

### 案例1：BTC短线趋势
- 胜率 55%，盈亏比 5%/3%
- 净优势 = 0.55×5 - 0.45×3 = 1.4%
- 建议仓位 = 1.4 ÷ 5 = 28%
- 执行½ = 14%

### 案例2：ETH资金费套利
- 胜率 70%，盈亏比 2%/1%
- 净优势 = 1.4 - 0.3 = 1.1%
- 建议仓位 = 55%
- 执行¼-½ = 14-27%

### 案例3：Meme热点
- 表面：胜率58%，盈亏比7%/5%
- 但1/6亏损是-25%插针
- 真实亏损 = 5/6×5% + 1/6×25% = 8.3%
- 新净优势 = 4.06 - 3.49 = 0.57%
- 建议仓位 ≈ 8% → 执行2-4%

---

## 8条铁律

1. **默认分数凯利**：先用½，带杠杆/不稳用¼
2. **摩擦全进账**：费率、滑点、资金费、Gas全部计入
3. **滚动估参**：月/季更新，重大事件临时降档
4. **三道闸门**：单笔、单日、单策略回撤硬阈值
5. **净敞口上限**：相关性高时顶层总仓要有硬帽
6. **极端日流程**：深度骤降/维护 → 切防守模板
7. **小样本慎重**：<200笔做保守收缩
8. **先截尾再放大**：先证明能控制最大亏损，再考虑放大

---

## 风险提示

- 凯利公式假设你能准确估计胜率和盈亏比
- 现实中有"肥尾"，历史数据不代表未来
- 分数凯利比全凯利更安全
- 杠杆交易有强平风险，必须先算安全边际

---

## 相关资源

- 原始文章：https://x.com/KKaWSB/status/1968453490084299020
- 论文：Kelly, J.L. (1956) "A New Interpretation of Information Rate"
- 书：Edward Thorp "Beat the Dealer", "Advances in Large Scale Actors"

---

## 更新日志

- 2026-03-20: 初始版本，包含核心公式、案例和铁律
