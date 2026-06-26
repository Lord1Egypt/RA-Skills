# ClawHub skill publish

Publish the **workflow skill** (`clawhub:identyclaw`) from this folder. For the **code plugin**, use root `npm run publish:clawhub`.

## Prerequisites

- `npx clawhub whoami` → access to publisher `@identyclaw`
- Sibling checkout: `../idclawserver-idc/references/` (or set `IDENTYCLAW_REFERENCES`)

## Steps

```bash
# from repository root
npm run skill:sync
npm run skill:publish:dry-run
npm run skill:publish
```

Bump `version:` in `skill/SKILL.md` frontmatter before each release. Changelog text is taken from root `CHANGELOG.md` when a matching version section exists.

## Install after publish

```bash
openclaw skills install clawhub:identyclaw
openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
```
