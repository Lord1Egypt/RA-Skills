# Releases & Versioning

## Semver: MAJOR.MINOR.PATCH
- MAJOR — breaking change (1.x → 2.0.0)
- MINOR — new feature, backward compatible (1.2.x → 1.3.0)
- PATCH — bug fix (1.2.3 → 1.2.4)

## Commands
```bash
gh release list --repo owner/repo

# ⚠️ CONFIRM WITH USER before running — creates a draft release (not yet public)
gh release create v1.3.0 --repo owner/repo --draft \
  --title "v1.3.0 — feature name" \
  --notes "## What's New\n- feat (#55)\n\n## Fixes\n- fix (#61)\n\n## Breaking\nNone"

# ⚠️ CONFIRM WITH USER before running — publishes a release to the repository
gh release create v1.3.0 --repo owner/repo \
  --title "v1.3.0 — feature name" \
  --notes "## What's New\n- feat (#55)\n\n## Fixes\n- fix (#61)\n\n## Breaking\nNone" \
  --target main

# ⚠️ CONFIRM WITH USER before running — publishes a pre-release (visible to all)
gh release create v2.0.0-rc.1 --repo owner/repo --prerelease

gh release upload v1.3.0 ./dist/binary --repo owner/repo  # attach artifact

# ⚠️ CONFIRM WITH USER before running — edits an existing release (title, notes, draft status)
gh release edit v1.3.0 --repo owner/repo --notes "Updated changelog"
gh release edit v1.3.0 --repo owner/repo --draft=false  # publish a draft release

# ⚠️ CONFIRM WITH USER before running — permanently deletes the release
gh release delete v1.3.0 --repo owner/repo --yes
```

## Tags
```bash
# ⚠️ CONFIRM WITH USER before running — pushes a tag to remote
git tag v1.3.0 && git push origin v1.3.0
gh api repos/owner/repo/git/refs --jq '.[] | select(.ref | startswith("refs/tags")) | .ref'
```
