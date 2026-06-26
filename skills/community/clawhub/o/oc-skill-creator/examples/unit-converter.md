# Example: unit-converter (Single Task)

The simplest skill type — no sub-agents, single execution, parameter parsing only.

## Characteristics
- No Phase 0 (simple lookup)
- No sub-agents
- Style Guide: N/A
- Core: natural language unit expression parsing + conversion table

## skill-audit Score: 75.9 (B-)
N/A: C+E → A(30%), B(20%), D(20%), F(30%)

## Skill Structure
```
unit-converter/
├── SKILL.md                              # 142 lines — conversion table + parsing rules
└── references/
    └── conversion-factors.md             # NIST-sourced exact conversion factors
```

## Lessons Learned
- Single-task skills can work with SKILL.md alone (references are optional)
- The conversion table itself acts as a "Style Guide" — accuracy criteria are inherent
- Low Workflow(D) score is natural — Phase 0 would be over-engineering for this type
