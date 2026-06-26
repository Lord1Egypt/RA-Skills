# Publishing to npm

## Table of Contents
1. [Manual publish](#1-manual-publish)
2. [GitHub Actions workflow (recommended)](#2-github-actions-workflow)
3. [npm provenance (required from May 2026)](#3-npm-provenance)
4. [Versioning strategy](#4-versioning-strategy)
5. [Submitting to n8n community](#5-submitting-to-n8n-community)
6. [Updating an existing package](#6-updating-an-existing-package)

---

## 1. Manual Publish

```bash
# One-time: log in to npm
npm login

# Bump version in package.json (pick one)
npm version patch   # 0.1.0 → 0.1.1  (bug fix)
npm version minor   # 0.1.0 → 0.2.0  (new feature, backwards compatible)
npm version major   # 0.1.0 → 1.0.0  (breaking change)

# Publish (prepublishOnly runs build + lint automatically)
npm publish --access public
```

The `--access public` flag is required for scoped packages (`@yourorg/n8n-nodes-...`). For unscoped packages it's optional but harmless.

---

## 2. GitHub Actions Workflow

Save as `.github/workflows/publish.yml` — triggers automatically when you push a version tag.

```yaml
name: Publish to npm

on:
  push:
    tags:
      - 'v*'     # triggers on v0.1.0, v1.0.0, etc.

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write    # required for provenance attestation

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Lint
        run: npm run lint

      - name: Publish with provenance
        run: npm publish --access public --provenance
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Publish flow:**
```bash
# Update version
npm version patch

# Push tag (triggers the workflow)
git push && git push --tags
```

---

## 3. npm Provenance

**Required for n8n community nodes from May 1, 2026.**

Provenance is a signed attestation from npm that the package was built by a specific GitHub Actions run — it proves the code in the package matches the code in the repo.

### Option A: Trusted Publishers (no token needed)

1. Go to [npmjs.com](https://www.npmjs.com) → your package → Settings → Publish access → Trusted Publishers
2. Click "Add a publisher"
3. Fill in:
   - **Repository owner**: your GitHub org or username
   - **Repository name**: your repo name
   - **Workflow filename**: `publish.yml`
4. Save — GitHub Actions can now publish without an `NPM_TOKEN` stored in secrets

Remove `NODE_AUTH_TOKEN` from the workflow when using Trusted Publishers.

### Option B: NPM Token (traditional)

1. Go to npmjs.com → Access Tokens → Generate New Token → Granular Access Token
2. Give it publish access to your package
3. Copy the token
4. In GitHub: repo Settings → Secrets → Actions → New repository secret
5. Name: `NPM_TOKEN`, value: the token

Keep `NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}` in the workflow.

---

## 4. Versioning Strategy

| Change type | Version bump | Notes |
|---|---|---|
| Bug fix, no interface change | `patch` (0.1.0 → 0.1.1) | |
| New operation, new optional field | `minor` (0.1.0 → 0.2.0) | |
| Renamed field, changed output structure | `major` (0.1.0 → 1.0.0) | Use node versioning too |
| First stable release | `1.0.0` | |

---

## 5. Submitting to n8n Community

After publishing to npm:

1. **Tag your package correctly** — `keywords: ["n8n-community-node-package"]` must be in `package.json`
2. **Submit to n8n Creator Hub**: https://n8n.io/creators — fill out the submission form
3. **Users install via**: n8n Settings → Community Nodes → Install → enter your npm package name

Your node will be installable immediately after publishing. The Creator Hub submission makes it discoverable in n8n's official directory.

---

## 6. Updating an Existing Package

```bash
# 1. Make your code changes
# 2. Build and test locally
npm run build

# 3. Bump version
npm version patch   # or minor / major

# 4. Publish
npm publish --access public
# OR push a tag to trigger GitHub Actions:
git push && git push --tags
```

Users who installed via n8n's community nodes UI will see an "Update available" badge in Settings → Community Nodes and can update with one click.

> ⚠️ If you made breaking changes (changed output structure, renamed fields), bump the major version AND add a node version increment — existing workflows using the old node will continue working on the old version.
