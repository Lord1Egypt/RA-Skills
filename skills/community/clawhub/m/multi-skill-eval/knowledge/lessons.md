# Evaluation Knowledge Base

## Lessons Learned (Accumulated Eval Wisdom)

### General
- Skills that rely on external credentials (dependency-gated) should be marked as such and evaluated separately from quality signals
- Phantom tooling (missing scripts) should be flagged separately from framework/template value
- Unsubstantiated marketing claims should be noted but not used in scoring

### Assertion Design
- Assertions that pass in both with-skill and without-skill are non-discriminating — always include skill-specific assertions
- Banned-word checks are highly discriminating for style-constrained skills (100% delta observed)
- For technical correctness tasks, baseline models are already strong — focus on methodology and structure, not correctness
- Bilingual keyword variants (Chinese + English) reduce false negatives for multilingual skills

### Category Patterns
- **Capability uplift skills**: target structural elements the model CAN produce but doesn't by default (excellent discriminators)
- **Framework-heavy skills**: can justify 50-90% time overhead IF they consistently improve actionability and formatting
- **CLI wrapper skills**: assert tool invocation, meaningful output delta, graceful dependency handling
- **Reference manual anti-pattern**: >200 lines of educational content — should be behavioral mandates instead
- **Library-as-skill anti-pattern**: code in SKILL.md instead of instructions — convert to behavioral guidance

### Efficiency
- Quality delta ≈ 0 but cost delta >2x should heavily penalize efficiency score
- Quick-mode routing reduces overhead for simple use cases