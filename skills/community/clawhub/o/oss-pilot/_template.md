# OSS Profile Template
#
# Copy this file to ./oss-pilot-data/profiles/<repo-name>.md
# Use the repo's short name (e.g., "cal.com.md", "dify.md", "ollama.md")
# Fill in the required fields. Optional sections grow as you contribute.

---
repo: owner/repo              # required -- e.g., calcom/cal.com
fork: YourUsername/repo        # required -- e.g., janedoe/cal.com
username: YourUsername         # required -- your GitHub username
local_path: ~/path/to/clone   # required -- where you cloned the fork
---

## Repo-Specific Rules
<!-- required -- start with build commands, add rules as you learn them -->
<!-- Example:
- Default branch: main
- Package manager: pnpm (monorepo with Turbo)
- Build/test: pnpm install && pnpm test
- Commit format: conventional commits (feat:, fix:, chore:)
- Max open PRs: 10 (bot auto-closes above this)
- Generated files: run `pnpm build:schema` after config changes, commit separately
- CLA required: yes (bot checks on first PR)
-->

## Architecture Patterns
<!-- optional -- add after first PR review teaches you what maintainers expect -->
<!-- Example:
- Data-driven > imperative: ordered arrays over nested conditionals
- Fix root causes in shared infrastructure, not symptoms in module-specific code
- Don't add special-case if branches -- extend existing data structures instead
-->

## Maintainer Review Styles
<!-- optional -- add after you get reviewed, note who cares about what -->
<!-- Example:
### @alice
- Focuses on data structure invariants and test coverage
- Requires changelog for user-visible changes
### @bob
- Prefers ordered arrays, rewrites nested conditionals
- Will rewrite your approach if he sees a better architecture (this is a compliment)
-->

## Bot Behavior
<!-- optional -- add after first PR, document each bot's name and behavior -->
<!-- Example:
### greptile-apps[bot] -- primary reviewer
- Confidence score 1-5, "safe to merge" verdict
- P1 = real bug, P2 = concern
### some-ci-bot -- hygiene enforcer
- Auto-closes for: dirty branch, too many PRs, stale
-->

## Label Taxonomy
<!-- optional -- add if repo uses structured labels for closures/triage -->
<!-- Example:
- `bug` -- confirmed bug
- `good first issue` -- maintainer invites contributions
- `close:not-planned` -- deliberate rejection, don't reattempt
-->

## Code Style
<!-- optional -- add conventions not captured by linter -->
<!-- Example:
- Files under ~700 LOC
- American English spelling
- No @ts-nocheck, no any
-->

## Testing Patterns
<!-- optional -- add repo-specific test conventions -->
<!-- Example:
- Colocated *.test.ts files
- Use vi.mock() not manual stubs
- Before/after evidence pattern
-->

## Live Verification
<!-- optional -- add if repo has dev server, browser testing, REPL -->
<!-- Example:
- Playwright MCP + dev server at localhost:3000
- After tests pass, capture UI screenshots for PR evidence
-->

## Lessons Learned
<!-- grows naturally -- oss-check retrospective appends here after each merged/closed PR -->
<!-- MAINTENANCE: when >15 entries, oss-check will prune lessons absorbed into
     Architecture Patterns, Maintainer Styles, or Bot Behavior sections.
     Keep entries that are still standalone insights not captured elsewhere. -->

## Gold Standard Examples
<!-- optional -- list 1-2 PRs that demonstrate ideal patterns for this repo -->
<!-- Example:
### Fast merge: PR #123 (~12 hours)
Concise ping format, clean scope, all bot comments answered.
### Bot iteration: PR #456 (3 rounds, merged)
Responded to every bot comment with commit hashes and evidence.
-->
