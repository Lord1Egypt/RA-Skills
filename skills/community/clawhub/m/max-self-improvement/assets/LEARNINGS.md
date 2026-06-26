# Learnings Template

This file serves as a template and index for learning entries.

---

## Quick Reference

### When to Log

| Situation | Category | File |
|-----------|----------|------|
| User correction | correction | LEARNINGS.md |
| Better approach found | best_practice | LEARNINGS.md |
| Outdated knowledge | knowledge_gap | LEARNINGS.md |
| Command failed | error | ERRORS.md |
| User requests feature | enhancement | FEATURE_REQUESTS.md |

### Entry ID Format

```
TYPE-YYYYMMDD-XXX
```

- TYPE: LRN | ERR | FEAT
- YYYYMMDD: Date
- XXX: Sequence or random

---

## Example Entries

### Learning Entry

```markdown
## [LRN-20260428-001] correction

**Logged**: 2026-04-28T21:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Code comments should use English

### Details
User said: "以后代码注释都用英文"

### Suggested Action
Change comment language to English by default

### Metadata
- Source: user_feedback
- Tags: style, consistency
```

### Error Entry

```markdown
## [ERR-20260428-001] bash_command

**Logged**: 2026-04-28T21:00:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
Docker deployment failed

### Error
Error: Missing DATABASE_URL environment variable

### Suggested Fix
Add environment variable configuration step

### Metadata
- Reproducible: yes
```

---

## Index

| ID | Category | Summary | Status | Date |
|----|----------|---------|--------|------|
| LRN-YYYYMMDD-XXX | category | summary | status | YYYY-MM-DD |
