# Failure Mode Catalog

## Evaluation Failures

### Non-Discriminating Assertions
- **Symptom**: Assertion passes with AND without skill
- **Root cause**: Assertion tests generic capability baseline already has
- **Fix**: Replace with skill-specific behavior assertion

### Phantom Tooling
- **Symptom**: SKILL.md references script X but file doesn't exist
- **Root cause**: Skill author documented aspirational tooling
- **Fix**: Separate framework/template evaluation from operational readiness

### False Negatives (Multilingual)
- **Symptom**: Chinese-language skill fails assertions in English
- **Root cause**: Model responds in Chinese, keyword checks miss it
- **Fix**: Add bilingual keyword variants

### Self-Grading Bias
- **Symptom**: Same model grades its own output
- **Root cause**: Execution model = judge model
- **Fix**: Use separate judge model from different provider

## Skill Quality Failures

### Reference Manual Anti-Pattern
- **Symptom**: SKILL.md is 200+ lines of educational content
- **Root cause**: Author wrote a textbook, not a skill
- **Fix**: Delete 70%+, add behavioral mandates (MUST/ALWAYS/NEVER)

### Library-as-Skill Anti-Pattern
- **Symptom**: SKILL.md contains Python/JS class definitions
- **Root cause**: Author wrote code instead of instructions
- **Fix**: Convert to behavioral instructions describing what the agent should do

### High-Overhead Framework Inflation
- **Symptom**: Quality delta ≈ 0 but time/token cost >2x baseline
- **Root cause**: Framework adds overhead without proportional benefit
- **Fix**: Add quick-mode routing or reject as not publishable