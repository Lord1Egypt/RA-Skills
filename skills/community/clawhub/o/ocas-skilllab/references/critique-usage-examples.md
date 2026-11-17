# Usage Examples

## Score a Single Skill

```bash
# Assess only (no changes)
Use critique.assess on the skill path.

# Full pipeline (score → fix → verify)
Use critique.run on the skill path.

# Iterate until 50/50
Use critique.iterate on the skill path.
```

## Score the Full Library

```bash
# Report only
python3 scripts/10khr_runner.py --report-only

# Identify current grinding target
python3 scripts/10khr_runner.py
```

## Grind a Specific Skill

```bash
critique.perfect ocas-forge    # single skill
critique.evolve ocas-rally     # same as .perfect
```

## Grind the Full Library Autonomously

```bash
critique.10khr
```

## Score Table Format

When printing the score table in Phase 2, use this format:

```
Skill Review: <name>
Path: <path>

| # | Dimension              | Score |
|---|------------------------|-------|
| 1 | Frontmatter            | ?/5   |
| 2 | Description Quality    | ?/5   |
| 3 | Conciseness            | ?/5   |
| 4 | Structure              | ?/5   |
| 5 | Instruction Clarity    | ?/5   |
| 6 | Freedom Calibration    | ?/5   |
| 7 | Error Handling         | ?/5   |
| 8 | Progressive Disclosure | ?/5   |
| 9 | Scripts Quality        | ?/5   |
|10 | Completeness           | ?/5   |
Overall: ?/50
```

## Code Ratio Measurement

```bash
python3 scripts/critique_code_ratio.py <skill>/SKILL.md
```

Target: under 20%. Over 30% = Major D3 issue.