# Publishing Guide

## Current State

- **npm package**: `@playasia/mcp` v0.1.0 (not yet published to npm)
- **ClawHub skill**: `playasia@0.1.0` (published, ID `k97bk5d1p3vhs8dpsk8vgfx25583xqg6`)
- **GitHub account**: `tom-playasia`

## Deploy to ClawHub

After any l402.php endpoint changes, update the skill listing:

1. Update `SKILL.md` with the new/changed endpoints
2. Bump version by `0.0.1` in `SKILL.md` frontmatter
3. Publish:

```bash
cd mcp-server
clawhub publish . --version X.Y.Z --slug playasia
```

The version in the publish command must match the `SKILL.md` frontmatter.

Slug: `playasia` (not `playasia-api` — that was squatted by `chinakingkong/mcp-server`)

## Publish to npm (when ready)

```bash
cd mcp-server

# Bump version in package.json + src/index.ts to match SKILL.md
npm run build
npm login          # one-time
npm publish --access public
```

After publishing, users install via `npx -y @playasia/mcp`.

MCP setup sections on `/account/access-tokens` and `/l402` are commented out — uncomment after npm publish.

## Pre-publish Checklist

- [ ] `SKILL.md` frontmatter version bumped by `0.0.1`
- [ ] `SKILL.md` documents all current endpoints
- [ ] No secrets or dev URLs in published files
- [ ] For npm: `package.json` version matches, `npm run build` succeeds
