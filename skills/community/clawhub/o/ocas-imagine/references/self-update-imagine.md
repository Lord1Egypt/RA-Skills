# Imagine — Self-Update Procedure

`imagine.update` pulls the latest package from GitHub. Runs silently.

1. Read `source:` from frontmatter → extract `{owner}/{repo}`
2. Read local version from frontmatter `metadata.version`
3. Fetch remote version via gh CLI
4. If versions match → stop silently
5. `cd {agent_root}/skills/ocas-imagine && git stash && git pull origin main && git stash pop`
6. On failure → retry once, then report error
7. Output: `I updated Imagine from version {old} to {new}`
