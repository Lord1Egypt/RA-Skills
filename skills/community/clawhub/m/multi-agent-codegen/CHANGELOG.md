# Multi-Agent Codegen 发布历史

## v3.3.0 (2026-09-24) — Test Verify Agent 接入

**关键升级**：给 `test_code.py` 加 L4 Verify 保护！

### 新增
- `State.verify_test_feedback` / `test_verify_retry_count` / `test_syntax_retry_count` 字段
- `Pipeline._run_test_verify_step()` 方法（对 test_code.py 跑 5 步规则验证）
- `Pipeline.__init__` 加 `max_test_verify_retries=3` 参数
- `notify_test_verify_done()` 飞书通知函数
- `TestAgent.run()` 支持 verify_test_feedback 注入

### 修复
- v3.2 只验证 code.py，导致 test_code.py SyntaxError 漏出
- v3.3 给 Test 产物也加 L4 Verify 保护（共用 max_hard_retries=5）

### 验证
- 简单 demo（字符串反转）：45 秒，82/100，verify (Write) + verify (Test) 双通过
- 健康检查 8/8 全过（含 15 项 L4 Verify 子检查）

---

## v3.2.0 (2026-09-23) — SyntaxError hard fail retry

**关键升级**：区分 hard fail vs soft fail，SyntaxError 走独立计数器

### 新增
- `Pipeline._classify_failure()` 方法（hard/soft 分类）
- `Pipeline.max_hard_retries=5`（SyntaxError 独立上限）
- `State.syntax_retry_count` 字段

### 改进
- `max_verify_retries` 默认 2 → 3（软错误给 LLM 更多机会）

### 修复
- LLM retry 后仍可能带 SyntaxError — 必须 hard fail 强制修复直到通过或达到 max_hard_retries

---

## v3.1.0 (2026-09-23) — L4 Verify Agent 接入主流水线

**关键升级**：Write Agent 完成后立即跑 5 步规则验证（长度/完整性/占位符/语法/密度）

### 新增
- `verify_agent.py` 模块（独立 L4 Verify Agent）
- `Pipeline._run_verify_step()` 方法
- `Pipeline.__init__` 加 `enable_verify` + `max_verify_retries` 参数
- `State.verify_feedback` + `verify_retry_count` 字段
- `notify_verify_done()` 飞书通知函数
- `WriteAgent.run()` 支持 verify_feedback 注入

### 遵循
- [RULE-20260701-001](https://my.feishu.cn/docx/Nw3RdgXR0oKVpSxyQRLcUG9nnm2) 终极根治 LLM retry 缩水

---

## v3.0.0 (2026-07-20) — 全程飞书通知

**关键升级**：6 节点飞书通知，老板在微信实时看到进度

### 新增
- 流水线启动/Plan/Write/Test/Refine/结束 6 个通知点
- 每个 Agent 完成立即推送飞书消息
- 不再是黑盒

---

## v2.0 (2026-06-22) — 初版

- 4-Agent 流水线（Plan/Write/Test/Refine）
- 单文件实现
- 半串行协作
