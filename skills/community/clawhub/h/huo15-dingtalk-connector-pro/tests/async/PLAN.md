# async（异步工具）测试方案

## 1. 目的与覆盖范围

`tests/async` 覆盖异步竞态与超时控制工具函数，主要验证 **raceWithTimeoutAndAbort** 在不同场景下的正确行为。

主要覆盖（以测试文件实际引用为准）：

- **raceWithTimeoutAndAbort**：Promise 竞态控制，支持超时和 AbortController 中止

## 2. 用例表（覆盖现有测试）

### 2.1 raceWithTimeoutAndAbort

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | Promise 先于超时解析 | 返回 `{ status: "success", value: "ok" }` |
| 2 | Promise 解析慢于超时 | 返回 `{ status: "timeout" }` |
| 3 | AbortSignal 已中止 | 返回 `{ status: "aborted" }` |
| 4 | AbortSignal 在解析前中止 | 返回 `{ status: "aborted" }` |
| 5 | Promise 被 reject | 抛出原始错误 |

## 3. 预期正确输出与潜在错误

- **正确**：竞态逻辑正确处理三种状态（success/timeout/aborted）；Promise 错误正确传播；超时和中止信号优先级正确。
- **潜在错误原因**：超时时间设置不当导致测试不稳定；AbortController 信号未正确清理；错误传播路径被意外捕获。
