# Example: changelog (Doc Conversion)

Transforms source data (git commits) into structured output (CHANGELOG.md).

## Characteristics
- Phase 0: repo analysis (commit range, version inference)
- No sub-agents (single pipeline)
- Style Guide: target (commit message preservation/compression criteria)
- Core: conventional commit parsing, category grouping, semver bump suggestion

## skill-audit Score: 85.1 (B+)
N/A: E → A(24%), B(18%), C(24%), D(18%), F(16%)

## Skill Structure
```
changelog/
├── SKILL.md                              # 126 lines — pipeline + commit parsing rules
└── references/
    └── conventional-commits.md           # Conventional Commits v1.0.0 summary
```

## Lessons Learned
- Style Guide connects naturally to parsing criteria (preserve original commit messages, compress similar ones)
- Clear phase numbering (Phase 0–4) raises Workflow(D) scores
- Good example of how to apply Style Guide to "partial target" skills
