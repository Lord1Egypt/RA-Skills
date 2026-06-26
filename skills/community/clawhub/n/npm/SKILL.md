---
name: npm
description: Use npm for package install, version inspection, dist-tags, and safe publish flows. Use when working on OpenClaw or ClawHub package releases, validating published versions, or handling npm auth/OTP publishing.
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "bins": ["npm"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "node",
              "bins": ["npm"],
              "label": "Install Node.js + npm (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "npm",
              "bins": ["npm"],
              "label": "Install npm (apt)",
            },
          ],
      },
  }
---

# npm

Use this skill for npm package operations with release-safe defaults.

## Scope

- OpenClaw packages in this monorepo (core + plugins)
- ClawHub CLI package/release checks when npm is involved
- npm publish, dist-tag, and version verification

## Guardrails

- Never publish from repo root unless explicitly requested for `openclaw`.
- For plugin-only releases, publish only changed plugins and keep `openclaw` untouched.
- For beta tags, publish matching beta versions (for example `2026.2.15-beta.1`) with `--tag beta`.
- Use `npm view <pkg> version --userconfig "$(mktemp)"` for read-only verification.
- If OTP is required, fetch it through the `1password` skill in tmux before publish.

## Quick Checks

```bash
npm --version
npm whoami
npm view openclaw version --userconfig "$(mktemp)"
```

## OpenClaw Release-safe Flow

1. Verify target package and local version:

```bash
npm view <package-name> version --userconfig "$(mktemp)"
node -p "require('./package.json').version"
```

2. Publish from package directory only:

```bash
cd <package-dir>
npm publish --access public --otp="<otp>"
```

3. Verify published version:

```bash
npm view <package-name> version --userconfig "$(mktemp)"
```

4. For beta releases:

```bash
npm publish --access public --tag beta --otp="<otp>"
```

## ClawHub Interop

- Use npm only for ClawHub package version/auth concerns.
- Use `clawhub` CLI for skill search/install/update/publish workflows.
- If both are needed: publish npm package first, then run `clawhub` publish/update commands.

## Useful Commands

```bash
# Inspect package metadata
npm view <package-name> dist-tags --json --userconfig "$(mktemp)"
npm view <package-name> versions --json --userconfig "$(mktemp)"

# Manage dist-tags
npm dist-tag add <package-name>@<version> beta
npm dist-tag add <package-name>@<version> latest

# Verify current auth context
npm whoami
npm profile get --json
```
