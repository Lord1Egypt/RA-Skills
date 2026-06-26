# Stock Research Quality Gate

这是当前 `kungfu_finance` 对 `stock-analysis-v2/quality_gate` 的 repo-controlled 收口版本。

## Current Gate Implementation

当前门禁由以下资产执行：

- `scripts/flows/research_shared/quality_gate.mjs`
- `tests/stock_research_flow.test.mjs`
- `tests/research_release_parity_contract.test.mjs`

## Gate Scope

- 报告标题、章节、`[事实]` / `[推演]` 分层
- 禁止出现具体交易指令
- SVG 根节点
- 阶段标签
- NOW 标记
- 主线 / 副线 / 推演线
- 估值区间
- 数据气泡数量
- 综合评级框

## Validation Entry

当前仓库统一通过以下命令进入门禁：

```bash
cd skills/kungfu_finance && npm test
```

如需只跑本轮 release parity 相关验证：

```bash
cd skills/kungfu_finance && node --test tests/research_release_parity_contract.test.mjs
```
