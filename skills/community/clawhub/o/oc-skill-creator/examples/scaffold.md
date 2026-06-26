# Example: scaffold (Code Generation)

Generates project structures, config files, and boilerplate.

## Characteristics
- Phase 0: requirements analysis (framework, language, package manager)
- No sub-agents (single generation)
- Style Guide: partial target (code preservation criteria)
- Core: framework-specific templates, existing file preservation

## skill-audit Score: 80.9 (B)
N/A: E → A(24%), B(18%), C(24%), D(18%), F(16%)

## Skill Structure
```
scaffold/
├── SKILL.md                              # 133 lines — structure + Phase 0 + config templates
└── references/
    └── framework-templates.md             # Next.js, Express, CLI, Docker templates
```

## Lessons Learned
- Preservation Criteria is key for code-gen ("never overwrite existing files")
- Phase 0 works well as "requirements analysis" here
- Separating templates into references/ makes SKILL.md flexible (easy to add new frameworks)
