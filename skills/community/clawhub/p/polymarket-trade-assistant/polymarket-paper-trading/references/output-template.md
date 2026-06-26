# 收益分析报告模板

保存路径：`~/polymarket-reports/performance-{YYYY-MM-DD}-{HHMMSS}.md`

---

## 报告头部

```markdown
# Polymarket 交易回测 — 收益分析报告

**报告时间：** {YYYY-MM-DD HH:MM:SS} (UTC)
**模式：** {纸上交易 / 实盘}
**运行天数：** {days} 天（自 {created_at}）

> {1-2 句话总结当前组合状态}
```

## 绩效概览

```markdown
## 绩效概览

| 指标 | 值 |
|------|-----|
| 初始资金 | ${initial_capital} |
| 当前总资产 | ${total_assets} |
| 总收益率 | {return_pct}% |
| 现金余额 | ${cash_balance} |
| 持仓市值 | ${positions_value} |
| 未实现损益 | ${unrealized_pnl} ({unrealized_pnl_pct}%) |
| 已实现损益 | ${realized_pnl} |
| 胜率 | {win_rate}%（{wins}/{total_settled}） |
| 最佳交易 | {best_trade_question} (+${best_pnl}) |
| 最差交易 | {worst_trade_question} (${worst_pnl}) |
| 活跃仓位 | {active_count} 个 |
| 挂单数 | {pending_count} 个 |
```

## 活跃仓位明细

```markdown
## 活跃仓位

| # | 市场 | 方向 | 进场价 | 当前价 | 份数 | 成本 | 市值 | 损益 | 损益% | 持有天数 | Edge |
|---|------|------|--------|--------|------|------|------|------|-------|---------|------|
| 1 | {question} | {dir} | ${entry} | ${current} | {shares} | ${cost} | ${value} | ${pnl} | {pnl%}% | {days} | {edge}% |
```

## 挂单明细

```markdown
## 挂单

| # | 市场 | 方向 | 限价 | 当前价 | 份数 | 冻结资金 | 挂单天数 | 状态 |
|---|------|------|------|--------|------|---------|---------|------|
| 1 | {question} | {dir} | ${limit} | ${current} | {shares} | ${reserved} | {days} | 待成交 |
```

## 已结算交易

```markdown
## 已结算交易

| # | 市场 | 方向 | 进场价 | 结算价 | 份数 | 损益 | 损益% | 持有天数 | 原始Edge | 结果 |
|---|------|------|--------|--------|------|------|-------|---------|---------|------|
| 1 | {question} | {dir} | ${entry} | ${exit} | {shares} | ${pnl} | {pnl%}% | {days} | {edge}% | {win/loss} |
```

## Edge 校准分析

```markdown
## Edge 校准分析

| 市场 | 预估Edge | 实际价格变动 | 偏差 | 准确性 |
|------|---------|------------|------|--------|
| {question} | {edge}% | {actual_move}% | {deviation}% | {准确/偏高/偏低} |

**平均 Edge 偏差：** {avg_deviation}%
**Edge-收益相关性：** {correlation}（正值 = 校准良好）
```

## 反思

```markdown
## 反思与改进

### 成功案例分析

{对每个盈利交易的分析：为什么预测准确？关键信息源是什么？}

### 失败案例分析

{对每个亏损交易的深度分析：}
- 失败原因：{信息不足 / 过度自信 / 结算标准误判 / 市场结构变化}
- 当时遗漏了什么信息？
- 如何避免类似错误？

### 策略回顾

**类别表现：**
- 政治类：{win_rate}% 胜率，{avg_pnl} 平均损益
- 加密类：{win_rate}% 胜率，{avg_pnl} 平均损益
- AI/科技类：{win_rate}% 胜率，{avg_pnl} 平均损益

**Longshot Bias 策略：**
- 买 No 交易数：{count}
- 买 No 胜率：{win_rate}%
- 买 No 平均损益：${avg_pnl}
- 评估：{该策略是否有效？是否应调整选股标准？}

**资金管理评估：**
- 平均仓位占比：{avg_position_pct}%
- 最大单笔仓位：{max_position_pct}%
- 是否触发过上限约束：{yes/no}
- 评估：{仓位大小是否合理？}

### 下一步调整建议

1. {具体可操作的调整建议}
2. {具体可操作的调整建议}
3. {具体可操作的调整建议}
```

## 报告尾部

```markdown
---

## 元数据

| 字段 | 值 |
|------|-----|
| 组合文件 | ~/polymarket-reports/portfolio.json |
| 模式 | {paper / live} |
| 初始资金 | ${initial_capital} |
| 运行天数 | {days} |
| 总交易数 | {total_trades} |
| 数据源 | Polymarket Gamma API + CLOB API |

**免责声明：** 本报告为回测分析，不构成投资建议。{若为纸上模式：所有交易为模拟，不涉及真实资金。}

---
*报告生成于 {YYYY-MM-DD HH:MM:SS} UTC*
```

## 格式规范

1. 所有金额带 $ 前缀，保留两位小数
2. 百分比保留一位小数
3. 损益正值用 `+` 前缀，负值自带 `-`
4. 时间使用 UTC，格式 YYYY-MM-DD HH:MM:SS
5. 反思部分必须引用具体数据，不可空泛
