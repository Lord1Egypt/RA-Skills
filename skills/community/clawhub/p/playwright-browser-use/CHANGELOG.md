# Changelog

All notable changes to `pw-browser` are documented here. This project follows semver-ish versioning (`MAJOR.MINOR.PATCH`).

## [1.3.11] — 2026-07-31

### Bug fixes

- **`act` DOM 变化检测遗漏"元素消失"**：此前只检测新元素出现（`appeared`），页面已有元素被移除或文本变更后 `act` 序列仍会用旧 ref 继续执行，导致 `ElementNotFound` 或误操作。现同时检测 `disappeared`（旧 ref 在新快照中消失），任一条件满足即中断序列并返回最新快照。
- **`run-code` 的 `vm.Script` 编译失败未返回结构化错误**：用户传入非法 JS 时，`new vm.Script()` 抛出的 SyntaxError 会被外层 `catch` 吞掉，daemon 返回 500 而非带 `kind: 'SyntaxError'` 的 JSON 错误。现在将编译步骤提前到独立 try/catch，失败时立即通过 `json()` 返回结构化错误并记录 `elapsedMs`。
- **客户端请求超时后 `res.on('end')` 可能双重回调**：`req.destroy()` 触发 `timeout` 事件后，`res` 端仍可能发来数据并触发 `end` 事件，导致 `resolve` 和 `reject` 都被调用（unhandled rejection 或错误结果）。引入 `settled` 守卫，确保 `resolve`/`reject` 仅被调用一次。

### Performance

- **`findElement` Strategy 1+2 合并**：`getByRole` 有 name 和无 name 原本是两段独立 if 块，会构造两次 Playwright locator。合并为一次查询（有 name 且 < 100 字符时带 name，否则不带），减少不必要的 locator 构造。
- **`ensurePage()` 过滤已关闭页面**：`context.pages()[0]` 可能拿到刚被关闭但尚未从 context 中移除的页面，后续操作会报错。改为 `filter(p => !p.isClosed())` 确保拿到的是有效页面。

### 文档

- **规则 1 澄清**：明确哪些情况必须 snap（每次导航/页面变更后），哪些情况可复用 ref（同一页面内连续操作），消除「每步 snap」与「不必每步 snap」之间的歧义
- **状态感知表 snap 描述修正**：ref 跨 snap 稳定的前提是「同一页面会话」，每次导航后必须重新 snap，旧 ref 不可复用
- **省 Token 建议补充导航条件**：「复用稳定 ref，不必每步重新 snap」改为「同一页面内复用稳定 ref，若页面发生导航（URL 变化、新页面打开），必须重新 snap」
- **storage 风险文档增强**：补充 SAFE_MODE=1 作为完全禁用 cookies/storage 的兜底措施说明，与代码实现在 v1.3.2+ 的行为对齐

## [1.3.10] — 2026-07-30
