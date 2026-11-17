# Security Review

Use this checklist before publishing a skill or adding release automation.

## Blockers

Stop and ask the user before publishing if any blocker appears:

- Private keys, tokens, passwords, cookies, recovery codes, or `.env` files are inside the skill or staged changes.
- Scripts read credential stores, SSH keys, browser profiles, shell history, OS keychains, or cloud credential files.
- Scripts upload files, call remote endpoints, or install remote code without the behavior being necessary and documented.
- Code is obfuscated, minified without source, dynamically decoded, or uses `eval` or equivalent execution on generated strings.
- Commands can delete broad paths, rewrite unrelated user files, or change global configuration.
- Large binaries or vendored dependencies appear without a clear purpose.

## Manual Checks

1. Inspect the target `SKILL.md` description. It should trigger only for the intended workflow.
2. List files under the target skill and explain why each resource directory exists.
3. Read every executable script in the skill before publishing.
4. Confirm scripts use local paths supplied by the user and avoid hard-coded personal directories.
5. Confirm references do not instruct agents to exfiltrate secrets, disable safeguards, or bypass user approval.
6. Confirm generated GitHub Actions never echo secrets and never commit generated credentials.

## Scanner Interpretation

`scripts/review_skill.py` is a first pass, not a complete audit.

- `ERROR` findings are publish blockers until resolved or explicitly accepted by the user.
- `WARN` findings require manual inspection and a short explanation in the final report.
- `INFO` findings are visibility notes such as large files or skipped binary content.

If the scanner is clean but the skill contains executable code, still read the scripts manually.
