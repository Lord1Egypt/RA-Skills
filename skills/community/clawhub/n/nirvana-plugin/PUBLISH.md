# PUBLISH.md — Publishing Nirvana to ClawHub

This guide walks through publishing Project Nirvana to ClawHub for distribution.

## Prerequisites

1. **ClawHub account** — https://clawhub.ai
2. **GitHub repository** — Public repo at `https://github.com/ShivaClaw/nirvana-plugin`
3. **OpenClaw CLI** — `openclaw` binary in PATH
4. **ClawHub CLI plugin** — Installed via OpenClaw skills
5. **Git repository** — Local git history with clean main branch

## Step 1: Verify Repository Structure

Ensure your repo has the required structure:

```
nirvana-plugin/
├── plugin-manifest.json      (plugin metadata)
├── config.schema.json         (configuration schema)
├── README.md                  (user documentation)
├── INSTALL.md                 (installation guide)
├── MIGRATION.md               (migration from cloud-only)
├── PUBLISH.md                 (this file)
├── src/
│   ├── index.js              (main plugin entry)
│   ├── ollama-manager.js      (Ollama lifecycle)
│   ├── router.js              (routing decision engine)
│   ├── context-stripper.js    (privacy boundary)
│   ├── privacy-auditor.js     (audit logging)
│   ├── response-integrator.js (cloud response caching)
│   ├── provider.js            (OpenClaw provider interface)
│   └── metrics-collector.js   (observability)
└── .git/                      (git repository)
```

## Step 2: Verify Plugin Manifest

Check `plugin-manifest.json` for completeness:

```json
{
  "id": "nirvana",
  "name": "Nirvana",
  "version": "0.1.0",
  "description": "Local-first AI sovereignty. Works out-of-box with bundled model (qwen2.5:7b). Privacy-preserving routing, zero API keys required. Cloud fallback optional.",
  "author": "ShivaClaw",
  "license": "MIT",
  "homepage": "https://github.com/ShivaClaw/nirvana-plugin",
  "repository": {
    "type": "git",
    "url": "https://github.com/ShivaClaw/nirvana-plugin.git"
  },
  "capabilities": [
    "local-inference",
    "privacy-enforcement",
    "query-routing",
    "context-stripping",
    "response-caching",
    "audit-logging"
  ],
  "permissions": {
    "models": ["read", "write"],
    "memory": ["read", "write"],
    "network": ["read"]
  },
  "main": "src/index.js",
  "type": "code-plugin"
}
```

## Step 3: Commit & Tag Release

Ensure all files are committed and tagged:

```bash
cd /data/.openclaw/workspace/nirvana-plugin

# Verify all files are staged
git status

# Commit if needed
git add -A
git commit -m "Project Nirvana v0.1.0: Ready for ClawHub publication"

# Create release tag
git tag -a v0.1.0 -m "Project Nirvana v0.1.0 - Local-first inference plugin"

# Push to GitHub
git push origin main
git push origin v0.1.0
```

## Step 4: Publish to ClawHub

### Option A: Using ClawHub CLI (Recommended)

```bash
# Install clawhub CLI if not already present
openclaw skills install clawhub

# Authenticate with ClawHub
clawhub auth login

# Publish the plugin
clawhub publish --path /data/.openclaw/workspace/nirvana-plugin

# Verify publication
clawhub search nirvana
clawhub info ShivaClaw/nirvana
```

### Option B: Manual ClawHub Dashboard

1. Navigate to https://clawhub.ai
2. Click "Publish Plugin"
3. Enter repository URL: `https://github.com/ShivaClaw/nirvana-plugin`
4. Select plugin type: **Code Plugin**
5. Fill in metadata:
   - **Name:** Nirvana
   - **Version:** 0.1.0
   - **Description:** Local-first AI sovereignty...
   - **Author:** ShivaClaw
   - **Tags:** local, privacy, inference, sovereignty
6. Review and submit
7. Wait for approval (typically 1-2 hours)

## Step 5: Verify Publication

After ClawHub confirms publication:

```bash
# List available plugins
clawhub search nirvana

# View plugin details
clawhub info ShivaClaw/nirvana

# Test installation
openclaw plugins install ShivaClaw/nirvana

# Verify plugin is loaded
openclaw gateway restart
openclaw status | grep nirvana
```

## Step 6: Announce Publication

Platforms to announce on:

1. **Moltbook** (@clawofshiva)
   - Post: "Nirvana is now available on ClawHub! 🎉"
   - Link: `https://clawhub.ai/ShivaClaw/nirvana`

2. **GitHub Discussions** (openclaw/openclaw)
   - Post release notes
   - Link to ClawHub

3. **Reddit** (r/openclaw)
   - Announce new plugin
   - Share features & benefits

4. **Discord** (OpenClaw community)
   - Share in #announcements channel

## Step 7: Post-Publication Maintenance

### Version Management

For future updates:

```bash
# Increment version in plugin-manifest.json
# e.g., 0.1.0 → 0.2.0

# Commit changes
git add -A
git commit -m "Nirvana v0.2.0: Add feature X, fix bug Y"

# Tag and push
git tag -a v0.2.0 -m "Nirvana v0.2.0"
git push origin main v0.2.0

# Publish to ClawHub
clawhub publish --path /data/.openclaw/workspace/nirvana-plugin
```

### Update Roadmap

Current planned updates:

- **v0.2.0:** Response integrator (pull cloud responses back to local memory)
- **v0.3.0:** Multi-model provider (support llama2, mistral, phi, etc.)
- **v0.4.0:** GPU acceleration (CUDA/Metal support detection)
- **v1.0.0:** Stable API, full test coverage, performance optimization

## Troubleshooting

### Plugin fails to publish

**Error:** `403 Unauthorized`
- Check ClawHub authentication: `clawhub auth status`
- Verify GitHub repository is public
- Ensure plugin-manifest.json is valid JSON

**Error:** `Repository not found`
- Verify GitHub URL in plugin-manifest.json
- Ensure repository is public
- Check that main branch exists and has commits

### Publication stalled

- Check ClawHub dashboard for approval status
- Email ClawHub support if stuck > 24 hours
- Verify plugin meets ClawHub code standards

### Installation fails after publication

```bash
# Verify plugin from ClawHub registry
clawhub search nirvana --details

# Test manual install from GitHub
openclaw plugins install https://github.com/ShivaClaw/nirvana-plugin

# Check gateway logs
openclaw gateway logs | grep nirvana
```

## ClawHub Metadata

**ClawHub ID:** (assigned on publication)  
**GitHub URL:** https://github.com/ShivaClaw/nirvana-plugin  
**License:** MIT  
**Author:** ShivaClaw  
**Categories:** AI Infrastructure, Privacy, Local-First  

---

## Checklist for Publication

- [ ] plugin-manifest.json is valid and complete
- [ ] All source files (src/*.js) are present and functional
- [ ] README.md is clear and up-to-date
- [ ] INSTALL.md provides working installation steps
- [ ] MIGRATION.md documents cloud→local migration path
- [ ] PUBLISH.md is complete (this file)
- [ ] GitHub repository is public and accessible
- [ ] Main branch is clean and ready for publication
- [ ] Git tags are created (v0.1.0, etc.)
- [ ] ClawHub account is active and authenticated
- [ ] Initial announcement is drafted

---

**Status:** Ready for ClawHub publication  
**Last Updated:** 2026-04-19 16:06 EDT  
**Publication Date:** Pending GitHub repo creation + ClawHub submission
