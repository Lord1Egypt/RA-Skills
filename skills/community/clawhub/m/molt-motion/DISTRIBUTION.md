# Molt Motion Skill Distribution

## Overview

The Molt Motion Skill is distributed through three channels to maximize accessibility and reach:

1. **GitHub** (Canonical source) - Primary release source with Git tags and GitHub Releases
2. **ClawHub** - AI skill registry for centralized discovery
3. **skills.sh** - Vercel-hosted skill directory

## Installation Options

### Option 1: GitHub (Recommended)

Install directly from the canonical GitHub repository:

```bash
npx @anthropic-ai/claude-cli skills install molt-motion \
  --github chefbc2k/MOLTSTUDIOS \
  --path moltmotion-skill
```

**Benefits:**
- Always up-to-date with latest release
- Full version history and changelog
- Direct access to source code
- GitHub Release notes with detailed changes

**View releases:** [github.com/chefbc2k/MOLTSTUDIOS/releases](https://github.com/chefbc2k/MOLTSTUDIOS/releases?q=moltmotion-skill)

### Option 2: ClawHub Registry

Install from ClawHub's centralized skill registry:

```bash
npx clawhub install molt-motion --registry https://clawhub.ai
```

**Benefits:**
- Centralized skill discovery
- Version verification
- Registry metadata
- Community ratings and reviews (future)

**View on ClawHub:** [clawhub.ai/skills/molt-motion](https://clawhub.ai/skills/molt-motion)

### Option 3: skills.sh (Vercel)

Browse and install via the skills.sh directory:

**Visit:** [skills.sh/s/chefbc2k/molt-motion](https://skills.sh/s/chefbc2k/molt-motion)

**Benefits:**
- Web-based browsing
- Installation instructions
- Visual documentation
- Cross-registry search

## Release Process

Releases are managed through the automated `bin/publish.sh` script:

```bash
# Bump patch version (default)
npm run publish-skill

# Bump minor version
./bin/publish.sh minor

# Bump major version
./bin/publish.sh major
```

### What the Release Script Does

1. **Version Bump**
   - Updates `package.json` version using semantic versioning
   - Commits version change to Git

2. **Git Tagging**
   - Creates annotated Git tag (e.g., `moltmotion-skill-v1.0.12`)
   - Pushes tag and commit to GitHub

3. **GitHub Release**
   - Creates GitHub Release with tag
   - Includes installation instructions for all three channels
   - Links to documentation
   - Generates release notes from commit history

4. **ClawHub Publish**
   - Publishes skill package to ClawHub registry
   - Updates registry metadata
   - Makes new version discoverable

5. **Installation Summary**
   - Prints all three installation commands
   - Displays GitHub Release URL
   - Shows version number

### Release Output

```
════════════════════════════════════════════════════════════════
  Molt Motion Skill Release Pipeline
════════════════════════════════════════════════════════════════

📦 Current version: v1.0.11
⬆️  Bumping patch version... v1.0.12
📝 Committing version bump...
🏷️  Creating Git tag... moltmotion-skill-v1.0.12
⬆️  Pushing to GitHub...
📦 Creating GitHub release...
📤 Publishing to ClawHub...

════════════════════════════════════════════════════════════════
  ✅ Release v1.0.12 Complete!
════════════════════════════════════════════════════════════════
```

## Version Strategy

The skill follows [Semantic Versioning](https://semver.org/):

- **Major (X.0.0)** - Breaking changes to skill API or behavior
- **Minor (1.X.0)** - New features, backward-compatible
- **Patch (1.0.X)** - Bug fixes, documentation updates

### When to Bump

- **Patch:** Bug fixes, documentation updates, minor improvements
- **Minor:** New API endpoints, new features, non-breaking enhancements
- **Major:** Breaking changes to skill interface, major API changes

## Distribution Channels in Code

### Web Client Integration

The skill install CTAs in the web client (`TheaterHero.tsx` and `XAccountDashboard.tsx`) show all three channels:

**TheaterHero.tsx:**
- Tab switcher between GitHub / ClawHub / skills.sh
- Dynamic install command based on selected channel
- Copy-to-clipboard for quick installation

**XAccountDashboard.tsx:**
- All three channels listed with copy buttons
- GitHub marked as "Recommended"
- Direct links to external registries

### Registry Configuration

**package.json:**
```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/chefbc2k/MOLTSTUDIOS.git",
    "directory": "moltmotion-skill"
  }
}
```

This ensures npm and other tools can resolve the canonical source.

## Verification

After release, verify the skill is available on all channels:

1. **GitHub Release**
   ```bash
   # View latest release
   gh release view --repo chefbc2k/MOLTSTUDIOS $(gh release list --repo chefbc2k/MOLTSTUDIOS --limit 1 | grep moltmotion-skill | awk '{print $3}')

   # Or view specific version (e.g., v1.0.12)
   gh release view moltmotion-skill-v1.0.12 --repo chefbc2k/MOLTSTUDIOS
   ```

2. **ClawHub Registry**
   ```bash
   npx clawhub search molt-motion
   ```

3. **GitHub Tag**
   ```bash
   git tag -l "moltmotion-skill-v*"
   ```

## Troubleshooting

### Release Script Fails

If the publish script fails:

1. Check GitHub authentication: `gh auth status`
2. Verify git remote: `git remote -v`
3. Ensure working directory is clean: `git status`
4. Verify npm credentials for ClawHub

### Version Conflict

If version already exists:

1. Manually bump version: `npm version patch --no-git-tag-version`
2. Commit change: `git commit -am "chore: bump version"`
3. Run publish script again

### GitHub Release Not Created

If GitHub CLI (`gh`) is not installed:

1. Install: `brew install gh` (macOS) or visit [cli.github.com](https://cli.github.com/)
2. Authenticate: `gh auth login`
3. Re-run publish script

## Future Enhancements

Planned improvements to distribution:

- [ ] Automated changelog generation from commits
- [ ] Pre-release / beta channel support
- [ ] npm registry publication (optional)
- [ ] Docker image for self-hosted deployments
- [ ] Homebrew formula for macOS users
- [ ] Auto-update notifications in skill itself
- [ ] Release verification tests (smoke tests post-publish)

## Support

For distribution issues:

- **GitHub Issues:** [github.com/chefbc2k/MOLTSTUDIOS/issues](https://github.com/chefbc2k/MOLTSTUDIOS/issues)
- **ClawHub Support:** Contact ClawHub registry team
- **skills.sh:** Visit skills.sh documentation
