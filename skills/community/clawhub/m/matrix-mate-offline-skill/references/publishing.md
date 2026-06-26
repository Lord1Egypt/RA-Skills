# Publishing Notes

Use this checklist to publish the exact same offline bundle to both skills.sh and ClawHub.

## Release artifact contract

The public bundle root must include:

- `SKILL.md`
- `README.md`
- `SECURITY.md`
- `agents/openai.yaml`
- `scripts/run-offline-mcp.mjs`
- `scripts/print-offline-mcp-config.mjs`
- `references/`
- `assets/examples/`
- `package.json`

## Preflight (required)

From repo root:

```bash
npm run skill:offline:build
npm run skill:offline:validate
npm test
```

If any command fails, do not publish.

## Export bundle

```bash
npm run skill:offline:export
```

This writes the publishable bundle to:

- `../skill-marketplace-repos/matrix-mate-offline-skill`

## skills.sh plan

1. Push `matrix-mate-offline-skill` mirror repo with a semver tag.
2. Ensure installer command works against the public mirror:
   - `npx skills add <owner>/matrix-mate-offline-skill`
3. Verify post-install runtime:
   - `npm install`
   - `node scripts/print-offline-mcp-config.mjs`
   - `node scripts/run-offline-mcp.mjs`
4. Confirm `SKILL.md`, `SECURITY.md`, and `README.md` stay in sync with the tagged release.

## ClawHub/OpenClaw plan

1. Publish the same exported bundle directory (no private files).
2. Keep semver aligned with the skills.sh tag.
3. Release notes should explicitly state:
   - local Matrix Mate app required
   - MCP transport is local stdio
   - browser flow is read/search-only
   - no hosted MCP URL in offline release
4. Run one smoke scenario in OpenClaw:
   - parse example Matrix link
   - fetch trip
   - export trip

## Poke recipe readiness

This bundle is recipe-ready at interface/doc level, but not live-publish-ready until a real hosted Matrix Mate MCP endpoint exists.

For future hosted recipe:

- keep read-focused behavior
- preserve the same trust boundary language
- switch MCP config to public URL only when stable and real
- publish separate hosted security notes
