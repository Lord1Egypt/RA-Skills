# Workflow 详细说明

## Round 执行流程

### 1. 并行 Spawn 3 个 Reviewer

| Reviewer | 关注点 |
|----------|--------|
| Reviewer-1 | 功能正确性、测试覆盖 |
| Reviewer-2 | 代码质量、最佳实践 |
| Reviewer-3 | 安全性、边界情况 |

### 2. 汇总结果，向用户报告

**必须向用户报告发现的问题。**

```
📊 Round N 完成
├─ 发现问题: X 个 (P0: a, P1: b, P2: c, P3: d)
└─ 下一步: [根据配置决定]
```

### 3. 根据配置决定下一步

读取自动化偏好：

```bash
PREF_FILE="$HOME/.openclaw/workspace/.iterative-code-review/preferences.json"
if [[ -f "$PREF_FILE" ]]; then
  CONFIG=$(cat "$PREF_FILE")
else
  CONFIG="{}"
fi

AUTO_FIX=$(echo "$CONFIG" | jq -r '.autoFix // false')
SEVERITY_THRESHOLD=$(echo "$CONFIG" | jq -r '.severityThreshold // "P0"')
```

| autoFix | 行为 |
|---------|------|
| `true` | 检查是否有问题 >= severityThreshold，有则自动 spawn Fixer |
| `false` | 询问用户是否继续修复 |

### 4. 用户确认后 Spawn Fixer

**只有 autoFix=false 时才需要用户确认。**

### 5. Fixer 完成后，根据配置决定下一步

| autoContinue | 行为 |
|--------------|------|
| `true` | 检查当前轮次 < maxRounds，自动进入下一轮 review |
| `false` | 询问用户是否继续 review |

### 6. 退出标准

- 连续 **两轮** 无 >= severityThreshold 的问题
- 或达到 maxRounds 限制
- 用户决定结束

---

## Final Round 特殊要求

**Final Round 必须采用 Full Review 模式！**

### 关键规则

1. **Final Round 必须 Full Review** - 不是 Delta Review
2. **必须验证编译和测试** - `npm run build` + `npm test`
3. **使用更长超时** - 全量审查需要更多时间
4. **审查所有历史修复** - 确认所有 Round 的问题都已修复