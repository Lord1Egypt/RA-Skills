# Self-Introspection

---

## What It Does

Before every answer, Context-Hawk automatically checks:

1. **Task clarity**: Is the current task clear?
2. **Information completeness**: Any missing required info?
3. **Context usage**: Is context near threshold?
4. **Loop detection**: Am I stuck in a repetitive cycle?
5. **Memory recall**: Should I recall relevant memories?

---

## Introspection Checklist

```markdown
[Context-Hawk] Introspection

1. Task Clarity
   ✅ Clear: "Complete the API documentation"
   ⚠️  Vague: "Work on the project"
   ❌  Unclear: task is blocked

2. Information Completeness
   ✅ Complete: requirements/specs/rules available
   ⚠️  Missing: [specific missing items]
   ❌  Severely incomplete

3. Context Usage
   📊 Current: 41% / Threshold: 80%
   ✅ Healthy: plenty of room

4. Loop Detection
   ✅ No loops detected
   ⚠️  Repeated failure on same issue
   ❌  Dead loop detected, intervention needed

5. Memory Recall
   💡 2 relevant memories available
   📎 Recent: "user prefers concise responses"
```

---

## Trigger Conditions

| Trigger | Condition |
|---------|-----------|
| Before every answer | context < 40% |
| Before every answer | context 40-60% |
| Before every answer | context > 60% |
| On user question | detects vague/missing info |
| On repeated failure | detects loop pattern |

---

## Introspection Output Formats

### Normal
```
[🦅 Introspection] ✅ OK
  Task: Complete API docs
  Context: 41%
  Suggestion: Continue
```

### Missing Information
```
[🦅 Introspection] ⚠️ Missing info
  Task: Implement payment module
  Missing:
    ❌ Payment interface spec (not designed yet)
    ❌ Third-party merchant credentials
  Suggestion:
    → Request technical spec from architect
    → Supply missing credentials
```

### Context High
```
[🦅 Introspection] 🔴 Context high
  Current: 78% / Threshold: 80%
  Largest: today.md (156 lines)
  Suggestion:
    → /hawk compress today summarize
    → /hawk strategy A
```

### Loop Detection
```
[🦅 Introspection] 🚨 Loop warning
  Detected: Same issue repeated 3 times
  Issue: Laravel transaction syntax
  Suggestion:
    → Check memory-longterm for "transaction" memories
    → Reference constitution.md line 12
```

---

## Commands

```bash
hawk introspect         # Immediate introspection
hawk introspect --deep  # Deep introspection (includes memory recall test)
hawk introspect --json  # JSON output
```

---

## Configuration

```json
{
  "introspection_enabled": true,
  "introspection_interval": "every_answer",
  "loop_detection_threshold": 3,
  "info_gap_check": true,
  "context_threshold_forced_check": 60
}
```
