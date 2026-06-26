# Contributing

Contributions welcome — especially new eval sets for popular OpenClaw skills.

---

## Adding Eval Sets

The most useful contribution is a well-crafted `evals/` directory for a skill that others use.

**Structure** (create `evals/<skill-name>/`):
```
evals/
└── <skill-name>/
    ├── triggers.json   ← Trigger Rate test cases
    └── quality.json    ← Quality Compare test cases
```

**Trigger test guidelines**:
- Include at least 5 positive (`"expected": true`) and 5 negative (`"expected": false`) cases
- Negative cases should be realistic queries that *shouldn't* trigger the skill
- Use `"category"` to group: `"positive"`, `"negative"`, `"edge-case"`

**Quality eval guidelines**:
- Write assertions against observable behavior, not model phrasing
- Use `"priority": true` only for assertions where failure = skill is broken
- Use `"note": "Best practice..."` for gap assertions (skill design issues, not execution errors)
- Aim for 3–8 assertions per eval; more is not better

---

## Reporting Issues

If a script fails or produces unexpected output, open an issue with:
- Which script and which `--mode`
- The error message or unexpected output
- Your OpenClaw version (`openclaw version`)
- A minimal `evals.json` that reproduces it

---

## Code Changes

- Keep Python scripts compatible with standard library + `requests` only
- `analyze_*.py` scripts must have **no** external dependencies (they run offline)
- Scripts must not call `sessions_spawn` — that is the agent's job (see `USAGE.md`)
- Add a `CHANGELOG.md` entry for any script changes
