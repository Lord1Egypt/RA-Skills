---
name: portfolio-review-polymarket-zh
version: 1.0.2
description: 审查 Polymarket 持仓组合，使用 EV 最大化框架。获取当前持仓，通过网络研究更新概率，应用 hold/sell/rotate 决策逻辑。当用户要求审查组合、评估仓位、优化持仓时使用此技能。
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": ["python3"]}}}
---

# Polymarket 持仓组合审查

使用 EV 最大化框架审查你的 Polymarket 组合。对每个仓位更新概率（基于最新网络研究），计算日化预期收益，排名仓位，产出 hold/sell/rotate 决策建议。

**核心原则：** 每天持有一个仓位 = 隐性地以当前价格重新买入。入场价是沉没成本，唯一重要的是当前 edge。

## 工作流程

按顺序执行以下 6 个步骤，不要跳过。

### 第 1 步：读取组合配置

读取组合配置文件以确定用户的钱包模式：

```
~/polymarket-reports/portfolio-address.md
```

文件包含：
- `username` — 报告中显示的用户名
- `wallet_address` — Polymarket 钱包地址 (0x...)

**如果文件不存在：**
1. 询问用户："您有 Polymarket 钱包地址吗？还是使用纸上组合模式（基于推荐历史记录）？"
2. 如果提供钱包地址 → 使用钱包模式
3. 如果选择纸上模式 → 使用 `--from-history` 读取 recommendation-history.md

### 第 2 步：获取当前持仓

运行持仓获取脚本：

**钱包模式：**
```bash
python3 scripts/fetch_portfolio.py --address 0x你的钱包地址 --output /tmp/portfolio-positions.json
```

**纸上模式（默认 — 基于最新 9 条推荐）：**
```bash
python3 scripts/fetch_portfolio.py --from-history ~/polymarket-reports/recommendation-history.md --latest 9 --output /tmp/portfolio-positions.json
```

脚本功能：
1. 解析推荐历史记录或获取钱包持仓
2. 去重同一市场的推荐（聚合仓位金额，加权平均入场价）
3. 通过模糊文本匹配将每个仓位对应到事件 slug
4. 从 Polymarket CLOB Midpoint API 获取当前价格
5. 计算盈亏、剩余天数和仓位详情
6. 输出结构化 JSON

**默认路径：** `--reports-dir ~/polymarket-reports/`

如果脚本运行失败，检查：
- 到 `gamma-api.polymarket.com` 和 `clob.polymarket.com` 的网络连接
- `recommendation-history.md` 是否存在且格式正确
- 是否至少存在一些包含 `polymarket.com/event/` URL 的 `market-pulse-*.md` 报告

### 第 3 步：保存持仓快照

读取第 2 步的 JSON 输出。格式化持仓数据并保存为快照文件：

**文件路径：** `~/polymarket-reports/portfolio-holding-{YYYY-MM-DD}-{HHMMSS}.md`

快照包含：
- 时间戳和组合模式
- 汇总表（总投入、当前价值、盈亏）
- 包含 JSON 中所有字段的仓位表

此快照作为审查时组合状态的历史记录。

### 第 4 步：研究与更新概率

**这是最关键的步骤。** 对每个仓位进行最新的网络研究，形成更新后的概率估算。

对每个仓位：

1. **网络搜索（2-3 次查询）：**
   - 搜索该事件的最新新闻
   - 搜索即将到来的催化剂或截止日期
   - 优先级：官方数据 > 权威媒体 > 专家分析

2. **更新概率（p_now）：**
   - 以当前市场价格作为先验
   - 根据每条证据更新（强烈转变: 10-20%，中等: 5-10%，微弱: 1-5%）
   - 指定置信度：高 / 中 / 低

3. **事件级思考（必需）：**
   - 自开仓以来发生了什么变化？
   - 原始论题是否仍然成立？
   - 有哪些即将到来的催化剂可能推动市场？
   - 是否有新的风险未反映在价格中？

记录所有信息源的 URL 和检索时间戳。

完整的 EV 最大化框架请参阅 [references/review-framework.md](references/review-framework.md)。

### 第 5 步：应用审查框架并生成报告

对每个仓位计算：

```
edge = p_now - c_now
daily_expected_return = (p_now - c_now) / (c_now × d_remaining)
f* = (p_now - c_now) / (1 - c_now)
f_q = f* / 4
```

其中：
- `p_now` = 更新后的概率估算（来自第 4 步）
- `c_now` = 当前市场价格（你持有方向的价格）
- `d_remaining` = 距市场结算的天数

**应用决策树：**

1. 如果 edge ≤ 0 → **卖出**（edge 已反转）
2. 如果论题崩塌 → **卖出**（无论 edge 如何）
3. 如果 daily_er < 0.02% 且存在更好机会 → **轮换**
4. 如果仓位 > 总资金 25% → 减仓（过度集中）
5. 如果单一主题 > 总资金 40% → 减少主题敞口
6. 否则 → **持有**

**按日化预期收益排名**所有仓位（从高到低）。

**日化收益解读：**
| 日化收益 | 评级 |
|----------|------|
| > 0.50% | 优秀 |
| 0.10% – 0.50% | 良好 |
| 0.02% – 0.10% | 边缘 |
| < 0.02% | 资金低效 |
| 负值 | 卖出 |

**轮换摩擦：** 仅在新仓位的 daily_er 比当前仓位高出至少 0.05%/天时才建议轮换（以覆盖约 2-4% 的价差/滑点损耗）。

**组合级检查：**
- Quarter-Kelly (f_q) 总和 ≤ 100%
- 单一主题 ≤ 总资金 40%
- 到期日分散
- 按优先级排序的行动摘要

按 [references/output-template.md](references/output-template.md) 中的模板格式化报告。

### 第 6 步：保存报告

将完整审查报告保存为 Markdown 文件：

```bash
mkdir -p ~/polymarket-reports
```

**文件路径：** `~/polymarket-reports/portfolio-review-report-{YYYY-MM-DD}-{HHMMSS}.md`

使用 Write 工具保存报告。保存后向用户确认文件路径。

**文件名示例：** `portfolio-review-report-2026-02-27-030000.md`

## 故障排除

- **脚本返回空仓位**：检查 recommendation-history.md 是否有 Open 状态的仓位。如果使用 `--latest 9`，尝试去掉该参数以包含所有开放仓位。
- **大量未匹配仓位**：slug 匹配依赖 pulse 报告文件。如果报告被删除，脚本无法提取 slug。手动在 Polymarket 搜索市场名称。
- **Midpoint 返回 None**：市场可能流动性极低或 CLOB API 不可用。脚本会回退到 Gamma API 的 `outcomePrices`。
- **聚合似乎不正确**：脚本按规范化市场名称 + 方向分组。检查相似市场名称是否正确分组。
- **没有 portfolio-address.md**：首次使用的用户属于正常情况。默认使用推荐历史的纸上模式。

## 参考文件

- [references/review-framework.md](references/review-framework.md) — EV 最大化决策框架
- [references/output-template.md](references/output-template.md) — 报告格式模板
- [references/polymarket-api.md](references/polymarket-api.md) — 完整 API 端点文档
