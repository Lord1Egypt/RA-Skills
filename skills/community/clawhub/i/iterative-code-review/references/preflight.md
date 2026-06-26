# Pre-flight Checks

开始 Review 前，必须执行以下检查并获得用户确认。

## Check 1: Model Selection

**用户选择或确认使用的模型。**

```
🔍 Model 选择

请选择用于 Code Review 的模型：
  - 输入模型 ID（如当前会话使用的模型）
  - 或直接回车使用当前模型

推荐：选择代码能力强的模型
```

**关键规则**：
- `thinking: "high"` - 建议启用，提高审查质量
- 用户决定使用哪个模型
- 不硬编码推荐任何特定模型

---

## Check 2: maxSpawnDepth

```bash
openclaw config get agents.defaults.subagents.maxSpawnDepth
```

| Value | Status |
|-------|--------|
| `≥1` | ✅ Proceed |
| `0` | ❌ Abort |

---

## Check 3: 变更规模检测

根据变更文件数调整超时时间：

| 规模 | 文件数 | Reviewer | Fixer | Final |
|------|--------|----------|-------|-------|
| 小型 | <10 | 4min | 6min | 8min |
| 中型 | 10-50 | 6min | 10min | 12min |
| 大型 | >50 | 10min | 16min | 20min |

---

## Check 4: 新增代码识别

```bash
git diff origin/develop HEAD --stat
git diff --name-only --diff-filter=A origin/develop HEAD
```

必须审查新增代码的安全性、测试覆盖、边界条件、资源清理。

---

## Check 5: PR 历史检查

```bash
git log --oneline origin/develop..HEAD
```

**关键**：读取 commit history，避免重复发现已修复的问题。

---

## Check 6: Review 模式选择

询问用户选择：
- **Full Review** - 审查所有变更
- **Delta Review** - 只审查最新 commit