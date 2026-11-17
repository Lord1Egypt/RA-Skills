# Sands — Self-Update Procedure

`sands.update` pulls the latest package from GitHub. Runs silently.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from frontmatter `metadata.version`
3. Fetch remote version: `gh api "repos/{owner}/{repo}/contents/SKILL.md" --jq '.content' | base64 -d | grep 'version:' | head -1`
4. If remote equals local → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once, then report error
7. Output exactly: `I updated Sands from version {old} to {new}`
