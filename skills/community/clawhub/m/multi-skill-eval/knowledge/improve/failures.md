# Failed Improvement Attempts

## What Doesn't Work

### Incremental content addition
- Adding more explanation to a skill that already has structural problems doesn't help
- Root cause: wrong paradigm, not insufficient detail

### Rewriting without diagnosis
- Blindly rewriting SKILL.md without first identifying root cause of failures wastes cycles
- Always diagnose before rewriting

### Trying to "improve" content that should be deleted
- Skills with reference-manual anti-pattern: adding more content (even "better" content) doesn't fix the problem
- The issue is verbosity and lack of behavioral directives, not content quality

### Over-engineering simple skills
- Simple CLI wrapper skills do not benefit from complex multi-step workflows
- Keep simple skills simple

## Known Failure Modes

1. **Same model grades own output** → confirmation bias, inflated scores
2. **>3 improvement cycles** → diminishing returns, need to document and move on
3. **Complex assertions on simple skills** → overhead without quality gain
4. **Ignoring phantom tooling** → operational failures in production
5. **Unsubstantiated claims as evidence** → circular self-referencing validation