# Example: skill-audit (Meta Validation Tool)

A meta-tool that evaluates other skills. Unique type, categorized separately.

## Characteristics
- No Phase 0 (simple Read → Score → Report)
- Sub-agents: optional (parallel when many targets)
- Style Guide: N/A, Sub-Agent Design: N/A
- Core: multi-dimensional scoring, N/A weight redistribution, batch mode

## Skill Structure
```
skill-audit/
├── SKILL.md                              # 6-dimension rubric + output format
└── references/
    ├── scoring-rubric.md                 # Detailed examples per dimension
    └── audits/                           # Completed audit reports
```

## Lessons Learned
- Meta-tools can self-audit — enabling quality loop checks
- N/A redistribution logic is critical — must cover 3 cases: C only, E only, C+E
- Differentiation from spec-based tools lies in quality scoring (Style Guide, Phase 0, sub-agent design), not structural validation
