# How to Publish olaxbt-nexus-data to ClawHub

Step-by-step instructions to publish this skill to [ClawHub](https://clawhub.ai) (the OpenClaw skill registry).

---

## Prerequisites

- **GitHub account** at least **1 week old** (ClawHub requirement).
- **Node.js** (for the ClawHub CLI) or use the ClawHub web app.
- This repo at a **clean, tagged state** you want to publish (e.g. `v1.0.0`).

---

## 1. Create a ClawHub account

1. Go to **https://clawhub.ai**
2. Click **Sign up** or **Publish a Skill**
3. Choose **Developer account** (for publishing)
4. Complete your profile:
   - Display name  
   - Bio  
   - Website (optional)  
   - **GitHub** (recommended; link your GitHub for credibility)
5. Verify your email

---

## 2. Pre-publish checklist

Before submitting, ensure:

- [ ] **Tests pass**
  ```bash
  cd olaxbt-nexus-data
  pip install -e ".[dev]"
  pytest tests/
  ```
- [ ] **No debug logging** or test-only code in the skill code
- [ ] **README.md** is clear (features, install, quick start, env vars)
- [ ] **SKILL.md** has valid YAML frontmatter and usage instructions
- [ ] **Version** is set in:
  - `.clawhub.yml` → `version`
  - `pyproject.toml` → `[project] version`
  - `SKILL.md` frontmatter if you use a version there
- [ ] **CHANGELOG.md** updated for this release (good for review and users)

### Permission justification (for review)

Your `.clawhub.yml` requests:

- **network** — Required for all OlaXBT API calls (auth + data). Only connects to `api.olaxbt.xyz` and `api-data.olaxbt.xyz`.
- **environment_variables** — Required for `NEXUS_JWT` only (obtain via Nexus auth flow; no private key in skill).

Be ready to explain each permission in the ClawHub submission form if asked.

### If ClawHub flags the skill as “suspicious”

The skill **does not request or use private keys**; it only requires `NEXUS_JWT`. Obtain the JWT using the [Nexus auth flow](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md) outside the skill. If the scanner still flags, appeal with a note that the skill is JWT-only (no ETH_PRIVATE_KEY).

---

## 3. `clawhub.json` (included)

**Where it’s needed:** The **ClawHub web app** (clawhub.ai → Publish New Skill) can auto-fill the listing form from **clawhub.json** when you upload your skill bundle. The CLI may use **.clawhub.yml** when you run `clawhub publish`.

This repo includes both:

- **.clawhub.yml** — Full metadata (permissions, requirements, compatibility) used by the CLI and tooling.
- **clawhub.json** — Listing fields (name, tagline, description, category, tags, version, license, support_url, homepage) used by the web UI.

When you bump a release, update **version** in both `.clawhub.yml` and `clawhub.json` (and `pyproject.toml`).

---

## 4. Optional: screenshots and demo (for marketplace listing)

For a stronger listing and faster approval:

- **Screenshots**: 3–5 PNGs (1920×1080 or 1280×720), e.g.:
  - Main use case (e.g. news output, market overview)
  - Env/setup (e.g. `.env` or config)
  - Example output (e.g. KOL heatmap or technical signals)
- **Demo video**: 30–90 seconds, real usage (e.g. install → set env → run example). Upload to YouTube/Vimeo and add the URL in the ClawHub form.

Put screenshots in a `screenshots/` folder in the repo if you want them in the bundle; otherwise upload them only in the web form.

---

## 5. Install the ClawHub CLI and log in

```bash
# Install CLI (pick one)
npm install -g clawhub
# or
pnpm add -g clawhub

# Log in (opens browser)
clawhub login
# Or with a token (e.g. for CI):
# clawhub login --token YOUR_TOKEN
```

Verify:

```bash
clawhub whoami
```

---

## 6. Exclude `.git` when publishing (avoid “SKILL.md required” error)

ClawHub can fail with “SKILL.md required” if the bundle includes a `.git` directory. This repo includes a **.clawhubignore** so that `.git` and other non-essential paths are not uploaded. If you publish from a **copy** of the repo without `.git`, you can skip this.

Otherwise ensure `.clawhubignore` exists with at least:

```
.git
.gitignore
*.pyc
__pycache__
.pytest_cache
.venv
venv
*.egg-info
```

---

## 7. Publish via CLI

From the **olaxbt-nexus-data** directory (or the path that contains `SKILL.md` and `.clawhub.yml`):

```bash
cd /path/to/olaxbt-nexus-data

# First time: publish with slug, name, version, and tag
clawhub publish . \
  --slug olaxbt-nexus-data \
  --name "OlaXBT Nexus Data" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Initial release. See CHANGELOG.md for details."
```

- Use the **exact version** that matches `.clawhub.yml` and `pyproject.toml`.
- If the CLI asks for a changelog and you didn’t pass `--changelog`, you can paste a short summary or “See CHANGELOG.md”.

**If publish still fails with “SKILL.md required”:**

- Publish from a **copy** of the repo that has no `.git` folder, or  
- Ensure `.clawhubignore` contains `.git` and run `clawhub publish` again.

---

## 8. Publish via ClawHub web app (alternative)

1. Go to **https://clawhub.ai** and sign in.
2. Open the **Developer** or **Publish** area.
3. **Package the skill** (without `.git` if possible):
   ```bash
   cd /path/to/olaxbt-nexus-data
   tar --exclude='.git' --exclude='.gitignore' -czf olaxbt-nexus-data.tar.gz .
   # Or zip the contents of the folder (no .git).
   ```
4. In the ClawHub UI:
   - **Upload** the archive (or follow the site’s “upload skill” flow).
   - Fill in metadata (name, tagline, description, category, tags, version, license, support URL, homepage). You can copy from `clawhub.json` or `.clawhub.yml`.
   - Upload **screenshots** and add **demo video URL** if you have them.
   - For each **permission** (network, environment_variables), add a short justification (see section 2).
5. Submit for **review**. Review often takes **2–5 business days**.

---

## 9. After submission

- **Review**: ClawHub may request changes (docs, permissions, or quality). Address every point, bump version if needed, update CHANGELOG, then resubmit.
- **Approval**: Once approved, the skill is public. Users can install it with:
  ```bash
  openclaw skill install olaxbt-nexus-data
  # or
  clawhub install olaxbt-nexus-data
  ```

---

## 10. Publishing updates (new versions)

1. Bump version in:
   - `.clawhub.yml` → `version`
   - `pyproject.toml` → `[project] version`
   - `clawhub.json` → `version` (if you use it)
2. Add an entry to **CHANGELOG.md**.
3. Publish again:

   ```bash
   cd /path/to/olaxbt-nexus-data
   clawhub publish . \
     --slug olaxbt-nexus-data \
     --name "OlaXBT Nexus Data" \
     --version 1.0.1 \
     --tags latest \
     --changelog "Bug fixes. See CHANGELOG.md."
   ```

   Updates are often reviewed faster than first-time submissions.

---

## Quick reference

| Step              | Action |
|-------------------|--------|
| Account           | clawhub.ai → Sign up → Developer account → Link GitHub |
| Pre-publish       | Tests pass, README/SKILL.md/CHANGELOG ok, permissions justified |
| CLI login         | `clawhub login` then `clawhub whoami` |
| Publish (CLI)     | `clawhub publish . --slug olaxbt-nexus-data --name "OlaXBT Nexus Data" --version 1.0.0 --tags latest` |
| If “SKILL.md” error | Use `.clawhubignore` with `.git` or publish from a copy without `.git` |
| Updates           | Bump version everywhere, update CHANGELOG, run `clawhub publish` again with new version |

---

## Links

- **ClawHub**: https://clawhub.ai  
- **OpenClaw ClawHub docs**: https://docs.openclaw.ai/tools/clawdhub  
- **This repo**: https://github.com/olaxbt/olaxbt-nexus-data  
- **Support**: https://github.com/olaxbt/olaxbt-nexus-data/issues  
