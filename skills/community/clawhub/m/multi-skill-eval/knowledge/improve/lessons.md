# Improvement Lessons (What Actually Works)

## Verified Improvements

### Deletion-first rewriting
- Skills that simply deleted 60-80% of content and added strong directives consistently improved more than those that tried to "improve" existing content
- The model has too much context already — less is more for behavioral control

### MUST/ALWAYS/NEVER directives work
- Vague guidance ("consider doing X") has near-zero behavioral effect
- Strong directives ("MUST do X before Y") significantly change agent behavior
- Best results: 1 directive per major step, max 10 directives total

### Quick-mode routing reduces overhead
- Adding a simple "if [simple case], use this fast path" reduced time cost by 40-60% for simple tasks
- No quality degradation observed for the targeted simple cases

### Bilingual assertions reduce false negatives
- Adding Chinese keyword variants alongside English reduced false negatives by ~30% for Chinese-language skills
- Cost: assertion complexity increases, but worth it for non-English skills

## Partial Success Patterns

### Framework-to-instructions conversion
- Partially effective — some code patterns converted well, others lost nuance
- Best for: CLI wrappers, data transformation helpers
- Poor for: complex stateful logic

### Phantom tooling replacement
- Works when the missing tool is simple (single command)
- Doesn't work when the tool encapsulates complex logic (rewrite just shifts complexity elsewhere)

## Failed Experiments

### Adding more examples to vague skills
- Adding examples to a skill that had structural problems (wrong paradigm) did not improve scores
- Fix the structure first, then add examples

### Multi-round iterative improvement
- Attempting >3 improvement cycles on the same skill rarely yields additional gains
- After 2 cycles with <0.5 point improvement, document limitations and move on

### Using the same model for improvement + eval
- Self-improvement introduces confirmation bias
- Best practice: use different model for improvement vs. grading