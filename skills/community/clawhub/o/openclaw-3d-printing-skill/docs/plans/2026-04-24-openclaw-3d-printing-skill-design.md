# OpenClaw 3D Printing Skill — Design

Date: 2026-04-24
Repo: `antoniosilveira/openclaw-3d-printing-skill`
Issue: #1

## 1. Goal

Publish the local `parametric-3d-printing` skill as a clean standalone open source project on Antonio's personal GitHub.

The project should be immediately usable by another OpenClaw user, easy to understand, and easy to package and share.

## 2. Design choice

Approved repo shape: **Option C**

This means:
- installable skill files at repo root
- `examples/` for practical usage examples
- `docs/` for planning and future lightweight project docs

## 3. Repository structure

```text
openclaw-3d-printing-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   ├── mesh_io.py
│   ├── preview.py
│   ├── run_cadquery_model.py
│   └── stl_to_3mf.py
├── references/
│   ├── design-review.md
│   └── requirements.txt
├── examples/
│   ├── simple-bracket.md
│   └── enclosure-brief.md
└── docs/
    └── plans/
        └── 2026-04-24-openclaw-3d-printing-skill-design.md
```

## 4. Content strategy

### Root level
- `SKILL.md` stays installable directly from the repository root.
- `README.md` explains what the skill does, how to install it into OpenClaw, the CadQuery dependency expectations, and how to package/test it.
- `LICENSE` will be MIT.
- `.gitignore` stays minimal and Python-oriented.

### `scripts/`
Keep the current runtime helpers as first-class project assets:
- model runner
- preview renderer
- STL loader/validation helper
- STL to 3MF converter

These stay small, readable, and usable outside the skill itself.

### `references/`
Keep detailed review and dependency guidance out of `SKILL.md` so the skill remains lean.

### `examples/`
Use examples as practical prompt inputs and expected usage patterns, not as long essays.

Planned v1 examples:
- `simple-bracket.md`
- `enclosure-brief.md`

### `docs/`
Keep docs intentionally light in v1.

Use `docs/` for:
- planning records
- later contributor notes if needed
- future release notes if the project grows

Do not bloat the repo with excessive documentation in v1.

## 5. Credit and attribution

The README should include a short explicit credit section:

- mention that this project was **inspired by** `flowful-ai/cad-skill`
- link to `https://github.com/flowful-ai/cad-skill`
- clarify that this repository is an **OpenClaw-native adaptation**, not an official fork or affiliated project

This keeps the inspiration visible without overstating equivalence.

## 6. Licensing

Use **MIT** for this repository, as requested.

Note: because the original inspiration project uses a different license posture, the README should be careful in wording:
- credit the inspiration
- avoid claiming code provenance unless we are intentionally copying exact code
- position this repo as a fresh OpenClaw-focused implementation inspired by the original approach

## 7. Initial implementation plan shape

The initial public release should include:
- root skill files and scripts
- MIT license
- README with install and usage instructions
- 2 small example briefs
- packaging validation

Not in v1:
- CI
- ClawHub publishing
- advanced test harness
- automatic CadQuery environment bootstrap

## 8. Demo requirement

Before calling the initial release complete, show:
- repository tree
- packaged `.skill` artifact generation
- README and attribution section

## 9. Recommendation

Proceed with this structure exactly as written.

It is simple, OpenClaw-native, and gives the project room to grow without feeling overbuilt.
