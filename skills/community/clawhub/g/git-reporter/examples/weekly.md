# Weekly Report 示例输出

以下是 `/git-reporter weekly` 的典型输出。

---

## Weekly Report — 2026-03-28 ~ 2026-04-04

> 本周重心在支付系统集成，完成了微信/支付宝双通道对接，同时修复了 3 个线上问题，测试覆盖率大幅提升

### Highlights（本周亮点）
- 完成微信支付和支付宝双通道的完整对接，进入内测阶段
- 修复了影响 2% 用户的 token 竞态条件（P1 级别）
- 测试覆盖率从 65% 提升至 90%，支付模块达到上线标准

### Breakdown（工作分类）

| 类别 | 数量 | 主要内容 |
|------|------|----------|
| Feature | 8 | 支付通道对接、订单分页、回调通知 |
| Fix | 3 | token 竞态、金额精度丢失、请求超时未重试 |
| Refactor | 2 | 支付回调统一抽象层、错误码标准化 |
| Test | 5 | 支付集成测试、回调 E2E、边界用例 |
| Docs | 1 | 支付模块 API 文档更新 |

### Change Heatmap（变更热区）
- `src/payment/` — 23 次变更（本周主战场）
- `tests/payment/` — 15 次变更
- `src/auth/` — 5 次变更
- `src/order/` — 3 次变更
- `docs/` — 1 次变更

### Carry Over（延续到下周）
- 支付对账系统的定时任务开发
- 微信支付的退款接口联调

### Risks & Notes
- **[Revert]** 周三回滚了一次金额计算的 float 精度修改，已用 Decimal 重新实现
- 支付宝沙箱环境本周有 2 次不可用，影响了联调进度

---
*19 commits across 5 days | 34 files changed | +1,247 -389*
