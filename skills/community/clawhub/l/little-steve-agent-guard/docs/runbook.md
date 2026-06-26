# Agent Guard Runbook

> **Security Notice**: This runbook includes manual bypass procedures for emergencies only.
> These procedures should be used by the human operator, never by the agent autonomously.
> For defense-in-depth, always combine guard-exec.sh with host-level controls
> (firewall, container network policy, filesystem permissions).

## Emergency Procedures

### 1. Circuit Break (Kill Switch)

If the guard itself is causing problems (false positives blocking all actions):

```bash
# Disable all active rules (keep core policy)
mv skills/little-steve-agent-guard/rules/active/*.rule /tmp/guard-rules-backup/ 2>/dev/null

# Verify: guard-exec.sh still works but only uses core policy checks
```

### 2. Rollback a Promoted Rule

```bash
bash skills/little-steve-agent-guard/scripts/promote-rule.sh demote --rule <rule-name>
```

### 3. Manual Takeover

If the agent is stuck in a prompt loop (L3 approval cycle):

```bash
# Execute the command directly, bypassing the guard
bash skills/<skill-name>/scripts/<script>.sh <args>

# Log the manual override
bash skills/little-steve-agent-guard/scripts/audit.sh log \
  --intent "manual_override" \
  --input "<command>" \
  --risk "high" \
  --decision "allow" \
  --evidence "human_manual_execution" \
  --outcome "success"
```

### 4. Reset Audit Log

If the audit log grows too large:

```bash
# Archive current log
mv reports/audit-events.jsonl reports/audit-events-$(date +%Y%m%d).jsonl.bak

# Start fresh (guard auto-creates)
```

### 5. Full Reset

Nuclear option — reset guard to factory state:

```bash
# Backup
cp -r skills/little-steve-agent-guard/reports /tmp/guard-reports-backup
cp -r skills/little-steve-agent-guard/rules /tmp/guard-rules-backup

# Reset
rm -f skills/little-steve-agent-guard/reports/audit-events.jsonl
rm -f skills/little-steve-agent-guard/reports/failure-dataset.json
rm -f skills/little-steve-agent-guard/rules/active/*.rule
rm -f skills/little-steve-agent-guard/rules/candidates/*.rule
```

## Routine Operations

### Weekly Review

```bash
bash skills/little-steve-agent-guard/scripts/weekly-report.sh generate 7
```

### Check Candidate Rules

```bash
bash skills/little-steve-agent-guard/scripts/promote-rule.sh list
```

### Test a Candidate Rule Before Promotion

```bash
bash skills/little-steve-agent-guard/scripts/replay-verify.sh test --rule <rule-name>
```

### Run Capability Diff on a Skill

```bash
bash skills/little-steve-agent-guard/scripts/capability-diff.sh check --skill-dir skills/<skill-name>
```

---

# 运行手册

## 紧急操作

### 1. 熔断（紧急停止）

如果 guard 自身导致问题（误拦截所有操作）：

```bash
# 禁用所有活跃规则（保留核心策略）
mv skills/little-steve-agent-guard/rules/active/*.rule /tmp/guard-rules-backup/ 2>/dev/null
```

### 2. 回滚已晋升规则

```bash
bash skills/little-steve-agent-guard/scripts/promote-rule.sh demote --rule <规则名>
```

### 3. 人工接管

如果 agent 陷入审批循环：

```bash
# 绕过 guard 直接执行
bash skills/<技能名>/scripts/<脚本>.sh <参数>
```

### 4. 重置审计日志

```bash
mv reports/audit-events.jsonl reports/audit-events-$(date +%Y%m%d).jsonl.bak
```

### 5. 完全重置

```bash
rm -f reports/audit-events.jsonl reports/failure-dataset.json
rm -f rules/active/*.rule rules/candidates/*.rule
```

## 日常操作

### 周报

```bash
bash scripts/weekly-report.sh generate 7
```

### 查看候选规则

```bash
bash scripts/promote-rule.sh list
```

### 测试候选规则

```bash
bash scripts/replay-verify.sh test --rule <规则名>
```

### 对技能做一致性检查

```bash
bash scripts/capability-diff.sh check --skill-dir skills/<技能名>
```
