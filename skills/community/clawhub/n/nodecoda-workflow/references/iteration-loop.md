# 迭代循环 — Build → 诊断 → 修复

> 写在 SKILL.md "6. 有界修复" 的细则。任何修 Source 的循环都遵守这里的纪律。

## 循环上限

| 项 | 上限 | 触发停止 |
|----|------|----------|
| Source 修复次数 | **5** | 第 6 次修复前停止整个任务 |
| admission 重试 | 3 | 第 4 次前停止 |
| 整体轮询 | 180 s | 超时后只调 1 次 `cancel_workflow_build` |
| 取消观察 | 35 s | 然后停止 |
| 诊断条数 | 100 | 超过即视为设计错误,停止 |

**违反上限** = 进入了"猜测性修改"区,会越改越糟。

## 单次迭代纪律

每次 Build → 诊断 → 修复 循环内必须满足:

1. **只修诊断指向的问题**
   - 诊断说 `TYPE_MISMATCH @ main.body[0].let.rhs`,你**只动那一个表达式**
   - 不顺手"美化"别的代码
2. **每次 Source 变化都换幂等 key**
   - 旧 key 用于"完全相同请求的不确定重放"
   - Source 变了哪怕一个字符,新 key
3. **记录这一轮的元数据**
   - Build ID
   - Source SHA-256
   - 修复前诊断摘要(只看 error 类,数 count)
   - 实际改的 location + 改了什么
4. **Source hash 与诊断重复即停**
   - 同一 Source hash + 同一诊断集合 = 没在动
5. **连续两次没严格减少 error 计数即停**
   - "error 数没下降" 不是 "error 重要程度下降"
   - "warning 变少" 不算 error 减少

## 修复模式(按诊断 code)

| 诊断类别 | 修复模式 |
|----------|----------|
| `SYNTAX_*` | 改 Source 语法;查 `language-reference.md` 确认关键字/分隔符 |
| `UNDEFINED_SYMBOL` / `SHADOWED_BINDING` | 改名字或补声明;**不**加 import(本语言不需要 import) |
| `TYPE_MISMATCH` / `INCOMPATIBLE_TYPES` | 改声明类型或显式 cast(若是支持的转换) |
| `MISSING_RETURN` | 补全每个分支的 return;**不**"为了过编译"塞 `return null` |
| `UNINITIALIZED_READ` | 加 `let` 初始化;**不**改用 `var` 绕 |
| `CAPABILITY_BLOCKED` / `TARGET_INCOMPATIBLE` | **不改 Source**;改设计或换目标 |
| `RESPONSE_CONTRACT_VIOLATION` | 调整 return/output/answer 写法使其符合 mode |
| `YIELD_OUTSIDE_LOOP` | 把 yield 移到 for 表达式体内 |
| `ARTIFACT_INVALID` / `CODEGEN_ERROR` | **不改 Source**;留 Build ID 报告主仓库 |

## 停止信号(必须遵守)

- 第 6 次修复前
- Source hash 不变
- 连续两次 error 计数没下降
- 出现 `CAPABILITY_BLOCKED` / `TARGET_INCOMPATIBLE`
- 出现 `POLICY` / `TARGET_UNAVAILABLE` / `SERVICE` / `TIMEOUT`(基础设施问题,不是 Source 问题)
- 任何 `DATA_INTEGRITY` 失败

## 状态机

```text
         ┌── error count 严格递减 ──┐
   iter  │                          ▼
   ──────▶ Build ──▶ Diagnose ──▶ Decide ──▶ Fix Source
            │           │           │            │
            │           │           │            └─▶ back to Build
            │           │           │
            │           │           └─── stop signal ──▶ Report
            │           │
            │           └─── FAILED.kind ∈ {POLICY, TIMEOUT, SERVICE, ...} ──▶ Report
            │
            └─── SUCCEEDED ──▶ Report
```

## 报告模板

停止时(成功或失败)输出:

```text
Outcome: SUCCEEDED | FAILED | CANCELLED
Build ID: <id>
target_profile: dify-1.16-graphon-0.6
duration: <ms>
Source SHA-256: <hash>
artifact SHA-256: <hash>           (only on SUCCEEDED)
diagnostics count: <n>             (last iteration)
repair iterations: <n>             (0..5)
stop reason: <one of: success, repair_budget, hash_unchanged, no_progress, capability_blocked, infra_failure, data_integrity>
next step: <human-readable>
unresolved dependencies: <list>    (Dify 端需要配置的 Model Provider / Tool / Knowledge dataset 等)
```

**禁止**:
- 在 Source 变更时复用旧幂等 key
- 在没看到诊断时盲改
- 在出现 `CAPABILITY_BLOCKED` 时改 Source
- 在 `repair iterations > 5` 后继续
