Scan a diff/patch for committed secrets — API keys, tokens, private keys — added lines only, values masked. Offline, zero deps.

`git diff --cached | node scripts/leak.js -`

Free lite version of `git-history-leak-check` — the full skill ($15) adds full-history scan + commit attribution. Also in the `security-audit-bundle-8-skills` bundle ($29). See SKILL.md for agent workflow.
