# Self-Improvement Logging Format

## Learning Entry

Append to `vault/60-learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX (if related)
---
```

**Categories:** correction, knowledge_gap, best_practice, workflow, tool_gotcha

## Error Entry

Append to `vault/60-learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
What failed

### Error
Actual error message or output

### Context
- Command attempted
- Parameters used
- Environment details

### Suggested Fix
What might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
---
```

## Feature Request Entry

Append to `vault/60-learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted

### User Context
Why they needed it

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How it could be built
---
```

## ID Format

`TYPE-YYYYMMDD-XXX` where TYPE is LRN/ERR/FEAT, XXX is sequential (001, 002...).

## Status Values

| Status | Meaning |
|--------|---------|
| pending | Not yet addressed |
| in_progress | Being worked on |
| resolved | Fixed (add Resolution block) |
| wont_fix | Decided not to address |
| promoted | Elevated to brain files |

## Priority Guide

| Priority | When |
|----------|------|
| critical | Blocks core functionality, data loss, security |
| high | Significant impact, common workflows, recurring |
| medium | Moderate impact, workaround exists |
| low | Minor, edge case, nice-to-have |

## Detection Triggers

Log automatically when you notice:
- **Corrections:** "No, that's wrong...", "Actually...", "That's outdated..."
- **Feature requests:** "Can you also...", "I wish you could...", "Is there a way to..."
- **Knowledge gaps:** User provides info you didn't know, docs are outdated
- **Errors:** Non-zero exit, exceptions, unexpected behavior, timeouts
