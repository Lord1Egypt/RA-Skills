# 输出模板

使用此模板生成持仓组合审查报告。

---

## 报告头部

```markdown
# Polymarket 持仓组合审查

**报告生成时间：** {YYYY-MM-DD HH:MM:SS} (UTC)
**组合模式：** {钱包 / 纸上}
**用户名：** {username 或 "N/A"}
**钱包地址：** {address 或 "基于 recommendation-history.md 的纸上组合"}

> {1-2 句执行摘要：组合整体健康状况，最优先行动}
```

## 组合概览

```markdown
---

## 组合概览

| 指标 | 数值 |
|------|------|
| 总仓位数 | {n} |
| 总投入 | ${total_invested} |
| 当前价值 | ${total_current_value} |
| **总盈亏** | **${total_pnl} ({total_pnl_pct}%)** |
| 最佳仓位 | {market} ({pnl_pct}%) |
| 最差仓位 | {market} ({pnl_pct}%) |
| 资金效率 | {avg_daily_er}% 日化收益（加权） |
```

## 仓位排名（按日化预期收益）

```markdown
---

## 仓位排名（按日化预期收益）

| 排名 | 市场 | 方向 | p_now | c_now | Edge | 日化收益 | 剩余天数 | 判决 |
|------|------|------|-------|-------|------|----------|----------|------|
| 1 | {market_truncated} | {Buy Yes/No} | {p_now}% | {c_now}% | {edge}% | {daily_er}% | {days} | {持有/卖出/轮换} |
| 2 | ... | | | | | | | |
| ... | | | | | | | | |

**图例：** 日化收益 > 0.50% = 优秀 | 0.10-0.50% = 良好 | 0.02-0.10% = 边缘 | < 0.02% = 低效 | 负值 = 卖出
```

## 逐仓位分析（对每个仓位重复）

```markdown
---

## {rank}. {market_question}

**链接：** https://polymarket.com/event/{event_slug}
**方向：** {Buy Yes/No} | **入场价：** {entry_price}% | **现价：** {current_price}%
**仓位：** ${position_usd}（{shares} 股） | **盈亏：** ${pnl} ({pnl_pct}%)
**到期日：** {end_date}（剩余 {days_remaining} 天）
**聚合自：** {n} 条推荐

### 更新概率评估

| | 市场价格 | AI 估算（更新后） | Edge |
|---|---|---|---|
| Yes | {market_yes}% | {ai_yes}% | {edge_yes} |
| No | {market_no}% | {ai_no}% | {edge_no} |

**置信度：** {高/中/低}

### EV 分析

| 指标 | 数值 |
|------|------|
| p_now（你持有的方向） | {p_now}% |
| c_now（当前价格） | {c_now}% |
| Edge | {edge}% |
| 日化预期收益 | {daily_er}% |
| Full Kelly (f*) | {f_star}% |
| Quarter Kelly (f_q) | {f_q}% |
| 评级 | {优秀/良好/边缘/低效/负值} |

### 事件级思考

{2-4 段分析：}

**最新动态：**
{自开仓以来发生了什么变化？新信息、事件、公告。}

**论题状态：**
{原始论题是否仍然成立？有哪些新风险或催化剂？}

**催化剂观察：**
{可能推动此市场的即将到来的事件：日期、决策、数据发布。}

### 判决：{持有 (HOLD) / 卖出 (SELL) / 轮换 (ROTATE)}

**理由：** {1-2 句解释决策}
{如果轮换："轮换至：{replacement_market} — 日化收益提升：{old}% → {new}%"}
{如果卖出："原因：{edge 反转 / 论题崩塌 / 过度集中 / 资金低效}"}

### 信息源

| # | 来源 | 检索时间 (UTC) | 关键发现 |
|---|------|----------------|----------|
| 1 | [{title}]({url}) | {YYYY-MM-DD HH:MM} | {finding} |
| 2 | [{title}]({url}) | {YYYY-MM-DD HH:MM} | {finding} |
| 3 | [{title}]({url}) | {YYYY-MM-DD HH:MM} | {finding} |
```

## 组合级分析

```markdown
---

## 组合级分析

### 集中度检查

| 主题 | 仓位数 | 总投入 | 占组合比例 | 状态 |
|------|--------|--------|-----------|------|
| {theme} | {n} | ${amount} | {pct}% | {正常 / 警告: >40%} |
| ... | | | | |

### 资金效率

| 指标 | 数值 |
|------|------|
| 加权平均日化收益 | {daily_er}% |
| 资金利用率 | 总资金的 {utilized}% |
| 日化收益 < 0.02% 的仓位 | {n} 个（${amount} 锁定） |
| 预估组合月度收益 | {monthly_return}% |

### Kelly 检查

| 指标 | 数值 |
|------|------|
| 总 f_q 之和 | {total_fq}% |
| 状态 | {正常: ≤100% / 警告: 超出 Kelly} |
| 最大单一仓位 | {market}，占总资金 {pct}% |

### 行动摘要

| # | 行动 | 市场 | 原因 |
|---|------|------|------|
| 1 | {持有/卖出/轮换} | {market} | {reason} |
| 2 | ... | | |
| ... | | | |

**优先行动：**
1. {最紧急的行动及具体细节}
2. {第二优先}
3. {第三优先}
```

## 报告尾部

```markdown
---

## 元数据

| 字段 | 数值 |
|------|------|
| 方法论 | 基于贝叶斯概率更新的 EV 最大化日化收益框架 |
| 分析师 | Claude AI |
| 报告版本 | 1.0 |
| 价格来源 | Polymarket CLOB Midpoint API + Gamma API |
| 框架 | 参见 references/review-framework.md |

**免责声明：** 此为信息分析，非投资建议。预测市场存在全额损失风险。过去表现不代表未来结果。

---
*报告生成于 {YYYY-MM-DD HH:MM:SS} UTC*
```

## 格式规则

1. 所有概率以百分比显示（如 35%，而非 0.35）
2. 所有金额带 $ 前缀和千位分隔符（如 $5,000）
3. Edge 值为带符号百分比（如 +15.0%、-3.2%）
4. 日化收益保留 2 位小数（如 0.15%）
5. 盈亏正值用 + 前缀，负值无前缀
6. 市场链接格式：`https://polymarket.com/event/{event_slug}`
7. 所有时间戳使用 UTC 时区，格式：YYYY-MM-DD HH:MM:SS
8. 每条信息源必须包含检索时间戳
9. 排名表中仓位按日化预期收益排序（最高在前）
10. 逐仓位分析章节按日化预期收益排序（最高在前）
11. 排名表中市场问题截断为 60 字符

## 文件保存约定

保存路径：`~/polymarket-reports/portfolio-review-report-{YYYY-MM-DD}-{HHMMSS}.md`

文件名示例：`portfolio-review-report-2026-02-27-030000.md`
