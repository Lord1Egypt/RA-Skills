<!--
  决策日志结构参考模板（仅供参考 / For Reference Only）。

  `.iterate_decisions.md` 由 AI 在 `/iterate` 会话中按 SKILL.md
  「决策日志格式 / Decision Log Format」章节创建并追加，本模板不经过
  CLI 生成器渲染。`{...}` 为 AI 填充的占位约定（与 SKILL.md 中的格式
  定义一致），不是 Python format 占位符。
-->

# Iterate Decision Log

Goal: {goal}
Max rounds: {maxRounds}
Started: {timestamp}
Branch: {iteration-branch}

---

## Round {N} — {timestamp}

### Atomic Fixes (Direct)

| # | File | Summary | Severity | Status |
|---|------|---------|----------|--------|
| 1 | | | | |

### Architectural Fixes (Approved + Executed)

| # | File(s) | Summary | Severity | Status |
|---|---------|---------|----------|--------|
| 1 | | | | |

### Architectural Fixes (Deferred to Next Round)

| # | File(s) | Summary | Defer Reason |
|---|---------|---------|-------------|
| 1 | | | |

### Reverted Fixes

| # | File(s) | Summary | Revert Reason |
|---|---------|---------|---------------|
| 1 | | | |

### AI Important Decisions

| # | Decision | Reason |
|---|---------|--------|
| 1 | | |

### Scope Dimension Redefinition (on-the-fly)

<!-- 只在未命中任何预设维度集、对偏门范围做 on-the-fly 重定义时才需要本段。
     每个维度的 Independent reason 必须是本范围特有的论证，不得照抄
     config/dimensions/<dim>.yaml 的默认 focus。scripts/validate.py 会据此校验。 -->
<!-- Only needed when an off-catalog scope was redefined on the fly. Each
     dimension's "Independent reason" must be scope-specific, not a copy of
     config/dimensions/<dim>.yaml's default focus (enforced by scripts/validate.py). -->

**Origin scope:** {redefined-scope}

| Dimension | Independent reason | Focus |
|-----------|-------------------|-------|
| security  | {why this scope needs it / independent rationale} | {scope-specific focus} |

### Validation

- 
