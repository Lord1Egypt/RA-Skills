# Learning Schema

## Files
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`

## Learning entry
```md
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: workflow | tools | product | growth | security | infra

### Summary
One-line learning

### Details
What happened and what is now understood

### Suggested Action
Specific next action

### Metadata
- Source: user_feedback | error | review | postmortem
- Related Files: path/to/file
- Tags: tag1, tag2
```

## Error entry
```md
## [ERR-YYYYMMDD-XXX] name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: infra | product | growth | security | ops

### Summary
What failed

### Error
Actual error or concise failure output

### Suggested Fix
Likely fix or next step

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file
```

## Feature request entry
```md
## [FEAT-YYYYMMDD-XXX] capability

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: product | ops | growth | security

### Requested Capability
What is missing

### User Context
Why it matters

### Suggested Implementation
Minimal implementation direction
```

## Experiment entry
```md
## [EXP-YYYYMMDD-XXX] experiment

**Logged**: ISO-8601 timestamp
**Priority**: medium | high | critical
**Status**: baseline | testing | keep | discard | partial_keep
**Area**: workflow | tools | product | growth | security | infra | ops

### Target
What repeated problem is being improved

### Baseline
What was failing before the change

### Mutation
The single change introduced

### Binary Evals
- [ ] Eval 1
- [ ] Eval 2
- [ ] Eval 3

### Result
What improved / did not improve

### Keep or Discard
keep | discard | partial_keep
```
