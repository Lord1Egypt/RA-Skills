---
name: NPM Package Scanner
description: Scan npm packages used in a repository for risk, maintenance health, and upgrade concerns.
metadata:
  openclaw:
    requires:
      bins:
        - rg
        - jq
        - bun
        - npm
---

# NPM Package Scanner

Use this skill when you need to inspect the npm packages used by a repository and identify security, maintenance, and dependency risks.

## Goal

Produce a practical package-risk review for the current repository:

- what dependencies are installed
- which ones are direct vs transitive
- which ones look stale, risky, or unnecessary
- whether there are known audit issues
- whether version ranges are too loose or outdated

## Scope

Focus on:

- `package.json`
- lockfiles such as `package-lock.json`, `bun.lock`, `pnpm-lock.yaml`, or `yarn.lock`
- workspace package manifests
- scripts that introduce package/tooling risk
- duplicated or overlapping dependencies

Use the reference notes in `references/checklist.md` and `references/commands.md` when useful.

## Workflow

1. Find package manifests and lockfiles.
2. Read the root `package.json` and any workspace manifests.
3. List direct dependencies and devDependencies.
4. Check for:
   - very old package versions
   - abandoned or suspicious packages
   - duplicate packages solving the same problem
   - unnecessary runtime dependencies
   - risky postinstall/build hooks
   - overly broad semver ranges
5. Run available package-manager audit commands if appropriate.
6. Summarize findings by severity.
7. Recommend concrete next steps.

## Commands

Prefer fast repo inspection first:

```bash
rg --files | rg '(^|/)(package\.json|package-lock\.json|bun\.lock|pnpm-lock\.yaml|yarn\.lock)$'
```

Inspect manifests:

```bash
cat package.json
```

If using Bun:

```bash
bun pm ls
bun audit
```

If using npm:

```bash
npm ls --depth=0
npm audit
```

If using pnpm:

```bash
pnpm ls --depth=0
pnpm audit
```

If using yarn:

```bash
yarn list --depth=0
yarn audit
```

## Output format

Return:

1. High-risk findings
2. Medium-risk findings
3. Low-risk cleanup items
4. Packages worth upgrading soon
5. Packages that may be removable
6. Exact commands to verify or fix

## Review rules

- Prioritize real risk over noise.
- Distinguish direct dependencies from transitive ones.
- Do not recommend upgrades blindly; mention likely blast radius.
- If audit output is noisy, extract only actionable items.
- If no serious issues are found, say so explicitly.

## Constraints

- Do not modify dependency versions unless explicitly asked.
- Do not remove packages unless explicitly asked.
- Do not assume a package is abandoned without evidence from the repo context or audit/tool output.
