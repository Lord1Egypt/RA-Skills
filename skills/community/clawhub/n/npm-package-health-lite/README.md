# npm-package-health-lite

Quick health check on an npm package before you install it — latest version, last publish age, deprecation flag, license, stale/deprecated heuristic. One registry request, zero deps, Node 18+.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill npm-package-health-lite
```

## Run

```bash
node scripts/health.js lodash
```

## Full version

The full `npm-package-health` skill ($7) adds weekly downloads, maintainer count, and dependency count. Ask for it by slug.
