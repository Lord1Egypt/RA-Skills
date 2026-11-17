# Reach — Self-Update Procedure

Standard GitHub tarball update via gh CLI. Runs silently.

1. Read `source:` from frontmatter → extract `{owner}/{repo}`
2. Read local version from frontmatter `metadata.version`
3. Fetch remote version via gh CLI
4. If versions match → stop silently
5. Download tarball, extract, copy files
6. On failure → retry once, then report error
7. Output: `I updated Reach from version {old} to {new}`
