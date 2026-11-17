---
name: npm-package-health-lite
description: Quick health check on an npm package before installing — latest version, days since last publish, deprecation flag, license, and a stale/deprecated heuristic. One unauthenticated registry request. Use when the user asks if an npm package is maintained or safe to add.
---

# npm Package Health (Lite)

## Network access (declared)

One GET to `registry.npmjs.org/<package>` — public registry metadata. No other hosts, nothing sent, no package installed, no code executed.

## Boundaries

- "Stale" is a heuristic on publish recency — quiet packages aren't necessarily abandoned.
- No weekly-download stats in this lite version (that is the full version's second API call).

## 1. Run

Requires Node 18+, zero dependencies.

```bash
node <skill-dir>/scripts/health.mjs <package-name>
```

JSON on stdout; exit `1` on fetch failure, `2` on missing argument.

## 2. Read the report

- `latest`, `lastPublish`, `ageDays`, `deprecated`, `license`, `health`.
- Flag: `deprecated` string present, `ageDays > 730`, `license: null`.

## 3. Report

```
<package>@<latest>: <health>
last publish Y days ago · license <spdx|none> · deprecated <yes/no>
<one-line recommendation: safe to add / pin version / consider alternative>
```

## Lite vs full

The full `npm-package-health` additionally reports weekly downloads (api.npmjs.org), maintainer count, and dependency count.
