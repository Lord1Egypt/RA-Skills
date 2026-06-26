# Publishing this skill to ClawHub

This bundle ships with tooling to make ClawHub validation painless.

## TL;DR

```bash
npm run validate     # smoke test: structure, references, ClawHub cleanliness
npm run pack         # produces ../ifq-design-clawhub-YYYY-MM-DD.tar.gz
```

Upload the resulting tarball (**not** the raw repo folder) to ClawHub.

## Why not upload the folder directly?

Some ClawHub validators walk the directory as-is and flag internal Git files
(`.git/kilo`, `.git/ORIG_HEAD`, `.git/config`) as "non-text files". They are
VCS metadata and must never be part of a published skill.

ClawHub's web uploader can also misclassify a hidden ignore file such as
`.clawignore` as a non-text artifact. This repo therefore uses
`clawhub.ignore.txt`: same purpose, but safe to keep inside the published skill
so `npm run validate` and `npm run pack` still work after install.

The `npm run pack` script reads `clawhub.ignore.txt` (gitignore-style) and builds a
deterministic `.tar.gz` that excludes:

- `.git/` and other VCS internals
- `.DS_Store`, editor junk, logs
- `node_modules/`, build output
- local `.env` and personal config
- OpenClaw local state (`.openclaw*/`)

The pack script also self-verifies — it will exit non-zero if any forbidden
entry slips into the final archive.

## ClawHub / VirusTotal posture

The safe bundle is designed to scan as plain source:

- zero npm dependencies in `package.json`
- zero npm install lifecycle hooks (`preinstall`, `install`, `postinstall`, `prepare`, publish hooks)
- zero script-side outbound connectivity primitives, enforced by `scripts/script-safety-rules.json`
- zero dynamic execution (`eval`, `new Function`) and no `child_process`
- no secrets, `.env`, personal asset indexes, VCS metadata, or hidden agent state in the archive
- default forkable templates do not rely on remote JS/CSS runtimes; optional showcase runtimes are pinned to exact versions; Google Fonts are optional Tier B progressive enhancement

The smoke script intentionally keeps deny-list literals in JSON data instead of inline code. This preserves local safety checks while avoiding ClawHub static-analysis false positives that combine file reads with scanner-only connectivity terms.

ClawHub pages display VirusTotal/OpenClaw scan summaries after upload. Treat the local checks as preflight, not as a replacement for the platform result.

## Listing and first-run checks

After upload, inspect the ClawHub page as a new user would:

- install path is visible and exact: `openclaw skills install ifq-design-skills`
- first-run prompt says to keep work scoped to this skill and inspect metadata before broader setup
- scanner summary reads as coherent across purpose, instruction scope, install mechanism, credentials, and persistence/privilege
- no required credentials are shown because this bundle has none
- examples make the safe output boundary obvious: HTML/SVG/static source here; MP4/GIF/PDF/PPTX automation only in the full GitHub repo

The `clawhub.json` `marketplace`, `first_run`, and `demo_artifacts` blocks exist to keep this listing experience machine-readable for OpenClaw agents and reviewable by humans.

## OpenClaw-friendly workflow

```bash
# 1. Validate locally
npm run validate

# 2. Produce a clean bundle
npm run pack

# 3. Inspect before upload (optional)
tar -tzf ../ifq-design-clawhub-*.tar.gz | head

# 4. Publish via OpenClaw
openclaw skills install ../ifq-design-clawhub-*.tar.gz
```

## Custom output path

```bash
node scripts/pack-skill.mjs --out /tmp/my-bundle.tar.gz
```
