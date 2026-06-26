# Contributing

This folder is the ClawHub-safe OpenClaw package. Keep it narrower than the full repo.

## Rules

- Do not add runtime dependencies.
- Do not add npm lifecycle hooks.
- Do not add script-side network calls.
- Do not add process-spawning scripts.
- Do not store secrets, signing certificates, `.env` files, or local OpenClaw state.
- Keep `SKILL.md` under 500 lines and keep `metadata:` as one JSON line.
- Keep `clawhub.json` and `SKILL.md` frontmatter in sync.
- Add or update an eval scenario when changing routing behavior.

## Before a PR

```bash
npm run validate
npm run validate:templates
npm run evals:validate
npm run pack
```

A ClawHub-ready change should pass all four locally.
