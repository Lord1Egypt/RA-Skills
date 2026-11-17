# npm-package-health-lite

Quick health check on an npm package before you install it — latest version, last publish age, deprecation flag, license, stale/deprecated heuristic. One registry request, zero deps, Node 18+.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill npm-package-health-lite
```

## Run

```bash
node scripts/health.mjs lodash
```

## Full version

The paid version adds weekly downloads, maintainer count, and dependency count:

- SkillHQ: https://skillhq.dev/skills/sone94/npm-package-health
- Agensi: https://agensi.io/skills/npm-package-health
