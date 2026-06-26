# IdentyClaw ClawHub skill

Workflow skill for OpenClaw agents. Published separately from the code plugin on ClawHub (`clawhub:identyclaw`).

## Layout

```text
skill/
├── SKILL.md              # ClawHub publish source (version in frontmatter)
├── references/           # gitignored — populated by skill:sync
└── scripts/
    ├── sync-references.mjs
    └── publish-clawhub.mjs
```

Reference docs are copied from **idclawserver-idc** at publish time (canonical API specs). Default path: `../idclawserver-idc/references`.

## Development

From repository root:

```bash
npm run skill:sync
npm run skill:publish:dry-run
npm run skill:publish
```

Override references source:

```bash
IDENTYCLAW_REFERENCES=/path/to/idclawserver-idc/references npm run skill:sync
```

## ClawHub

- Skill: `openclaw skills install clawhub:identyclaw`
- Plugin: `openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin`

See [PUBLISH.md](./PUBLISH.md) and root [PUBLISH.md](../PUBLISH.md) for ClawHub auth.
