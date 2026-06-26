---
name: back-testing-predmarket-zh
version: 1.0.2
description: 回测 Polymarket 推荐历史。获取当前市价，计算每笔历史推荐的盈亏，按类别和方向评估收益，并生成策略反思报告。当用户要求回测、评估表现、查看收益、分析 Polymarket 推荐盈亏时使用此技能。
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["python3"]}}}
---

# Polymarket 推荐回测

评估所有历史 Polymarket 推荐的表现：获取实时市价，计算每笔仓位的盈亏，按类别和方向分析收益，生成策略反思报告。

## 工作流程

按顺序执行以下 5 个步骤。

### 第 1 步：运行回测脚本

运行回测脚本，解析历史记录、获取当前价格、计算盈亏：

```bash
python3 scripts/backtest.py --output /tmp/backtest-results.json
```

脚本功能：
1. 解析 `~/polymarket-reports/recommendation-history.md`（全部历史推荐）
2. 扫描 `~/polymarket-reports/market-pulse-*.md` 文件，从 URL 中提取事件 slug
3. 通过模糊文本匹配将每条推荐对应到事件 slug
4. 从 Polymarket Gamma API 和 CLOB midpoint API 获取当前价格
5. 计算每笔仓位的盈亏（未结算为未实现盈亏，已结算为已实现盈亏）
6. 输出结构化 JSON，包含逐仓位明细和汇总统计

**默认路径：** `--history ~/polymarket-reports/recommendation-history.md`，`--reports-dir ~/polymarket-reports/`

如果脚本运行失败，检查：
- 到 `gamma-api.polymarket.com` 和 `clob.polymarket.com` 的网络连接
- `recommendation-history.md` 是否存在且格式正确
- 是否至少存在一些包含 `polymarket.com/event/` URL 的 `market-pulse-*.md` 报告

### 第 2 步：审查数据质量

读取 JSON 输出并检查：

1. **未匹配记录** — `unmatched` 数组列出无法匹配到事件 slug 的市场。对每条：
   - 尝试在 Polymarket 上手动查找事件 slug
   - 如果找到，记录正确价格以纳入报告
   - 如果确实无法获取，在报告中标注"数据不可用"

2. **异常盈亏** — 检查极端异常值（> 500% 盈利或 > 100% 亏损），可能原因：
   - Token ID 匹配错误（多市场事件交叉匹配）
   - 市场在上次检查后已结算
   - 价格数据过时或缺失

3. **已结算市场** — `resolved_status` 为 "won" 或 "lost" 的记录，应在第 4 步更新状态。

### 第 3 步：生成回测报告

按 [references/output-template.md](references/output-template.md) 中的模板格式化结果。

报告必须包含：

1. **绩效概览** — 总投入、当前价值、总盈亏（已实现 + 未实现）、胜率
2. **仓位明细** — 逐推荐分解，含入场价、现价、盈亏、持仓天数
3. **分类分析** — 按市场类别分组（加密、地缘政治、体育、科技、政治）
4. **方向分析** — Buy Yes 与 Buy No 的表现对比
5. **Edge 校准** — 对比 AI 预估 edge 与实际回报
6. **策略反思** — AI 生成的分析，涵盖：
   - 表现最好和最差的推荐及根因分析
   - 类别级洞察（哪些主题预测更准确？）
   - Longshot bias 验证（低 Yes 价市场的 Buy No 是否跑赢？）
   - 仓位管理评估（凯利仓位是否优于固定仓位？）
   - 3-5 条具体可执行的改进建议

**时间戳：** 所有时间使用 UTC，格式 `YYYY-MM-DD HH:MM:SS`。

### 第 4 步：更新推荐历史

对已结算市场（赢/输），更新 `~/polymarket-reports/recommendation-history.md`：
- 将 Status 列从 "Open" 改为 "Won" 或 "Lost"
- 使用 Edit 工具进行定向替换
- 不修改其他列

### 第 5 步：保存报告

将回测报告保存为 Markdown 文件：

```bash
mkdir -p ~/polymarket-reports
```

**文件路径：** `~/polymarket-reports/backtest-{YYYY-MM-DD}-{HHMMSS}.md`

使用 Write 工具保存。保存后向用户确认文件路径。

## 故障排除

- **大量未匹配记录**：slug 匹配依赖 `~/polymarket-reports/` 中的 pulse 报告文件。如果报告被删除，脚本无法提取 slug。手动在 Polymarket 搜索市场名称。
- **Midpoint 返回 None**：市场可能流动性极低或 CLOB API 不可用。脚本会回退到 Gamma API 的 `outcomePrices`。
- **价格过时**：Gamma API 的 `outcomePrices` 可能滞后于 CLOB midpoint。如需精确数据，请在 Polymarket 网站验证。
- **脚本超时**：20+ 个唯一事件需要约 40-60 次 API 调用，可能需要 30-60 秒。

## 参考文件

- [references/output-template.md](references/output-template.md) — 报告格式模板
