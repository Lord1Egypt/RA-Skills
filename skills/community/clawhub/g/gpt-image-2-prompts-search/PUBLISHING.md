# Publishing Guide

This skill auto-publishes to [ClawHub](https://clawhub.ai/skill/gpt-image-2-prompts-search) when a version bump lands on `main`. No manual `clawhub publish` needed.

## How It Works

**Split distribution model:**

| Layer | What | Where | How updated |
|-------|------|-------|-------------|
| **Code** | `SKILL.md`, `setup.js`, `package.json` | ClawHub | Auto via `.github/workflows/publish.yml` |
| **Data** | `references/*.json` (large) | GitHub (this repo) | Auto via `.github/workflows/generate-references.yml` (twice daily) |

Data files never go to ClawHub — `scripts/setup.js` downloads them from GitHub at install time via `postinstall`.

---

## Publishing a New Version

1. **Bump the version** in `SKILL.md` frontmatter:
   ```yaml
   ---
   name: gpt-image-2-prompts-search
   version: 1.1.0   # ← bump this
   ---
   ```
2. Open a PR, get it reviewed, merge to `main`.
3. The **Publish to ClawHub** workflow runs automatically:
   - Reads `version:` from SKILL.md
   - Compares to ClawHub's current version
   - If different → packages (honoring `.clawhubignore`) and publishes
   - If same → skips
4. Force republish (same version): Actions → Publish to ClawHub → Run workflow → check `force`.

---

## Required GitHub Secrets

| Secret | Purpose |
|--------|---------|
| `CMS_HOST` | PayloadCMS API host (for `generate-references`) |
| `CMS_API_KEY` | PayloadCMS API key (for `generate-references`) |
| `YOUMIND_CLAWHUB_TOKEN` | ClawHub publish token (for `publish`) |

---

## What Gets Packaged

Controlled by `.clawhubignore`. Included:

| File | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions |
| `README.md` | Human-readable docs |
| `package.json` | Metadata, postinstall hook |
| `scripts/setup.js` | Downloads references from GitHub at install time |
| `references/manifest.json` | Category directory |

Excluded: `references/*.json` (except manifest), `scripts/generate-references.ts`, `.github/`, `node_modules/`.

---

## Data Updates (Fully Automatic)

- **Schedule**: twice daily at 00:00 / 12:00 UTC via GitHub Actions
- **First run**: also triggered when `scripts/generate-references.ts` is pushed
- **Users stay fresh**: `setup.js --check` silently refreshes their local copy every 24h
- **Force a sync**: Actions → Generate References → Run workflow

No ClawHub republish needed when data updates — the version on ClawHub stays constant, and clients pull fresh data from GitHub on their own.

---

## ClawHub Skill Page

https://clawhub.ai/skill/gpt-image-2-prompts-search
