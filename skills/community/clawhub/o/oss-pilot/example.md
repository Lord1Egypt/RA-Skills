# Example Profile: A Large TypeScript OSS Project
#
# This is a real profile built from 5+ PRs of contributions.
# It demonstrates what a mature profile looks like after the
# learning loop has been running for several weeks.
#
# Your profile will start nearly empty (from _template.md) and
# grow naturally as you contribute.

---
repo: example-org/example-project
fork: your-username/example-project
username: your-username
local_path: ~/example-project
---

## Repo-Specific Rules
- Max open PRs: 10 (hygiene bot auto-closes above this -- no warning, just closes)
- Commit script: `scripts/committer` (runs full lint/format/check suite before committing)
- Generated files: run `pnpm config:schema:gen` and `pnpm config:docs:gen` after config changes, commit separately
- Always run `pnpm format:fix` before committing -- formatter has strict line-breaking rules that differ from editor auto-format
- Pre-rebase: check main CI is green first, don't rebase onto broken main
- PR description must include: Summary, What did NOT change, Security Impact, Evidence, What I Did NOT Verify, Failure Recovery
- Don't use `@ts-nocheck`, `@ts-ignore`, or `any` -- never disable `no-explicit-any`
- American English spelling (color not colour)
- Issue references use plain `#24643` (not backticked) for auto-linking
- PR template exists at `.github/pull_request_template.md` -- follow it exactly
- Extensions directory (`extensions/`) is the key modular area for scoped contributions -- lower blast radius, dedicated maintainers, faster review
- Extension-specific CI check (`extension-fast`) provides quick feedback for extension changes

## Architecture Patterns (with examples)
- **Data-driven > imperative**: ordered arrays over nested conditionals. Example: maintainer rewrote a contributor's IP fallback from nested conditionals to ordered array.
- **Fix root causes in shared infrastructure, not symptoms in module-specific code**: Example: a channel-specific EADDRINUSE fix was moved from a guard to the shared gateway channel manager. Another contributor disabled a feature to "fix" startup failure, but the real issue was noisy retry logs -- rejected.
- **Trace call chains 3-5 levels deep**: Example: an `includes("/")` guard seemed correct at the UI layer but failed for vendor-prefixed model IDs because the server's parser splits at the first "/". Only tracing server->session->API chain revealed the correct fix.
- **Don't add special-case if branches** -- extend existing data structures instead
- **Preserve semantic contracts**: Maintainers focus on data structure invariants. Examples: truncation breaking compaction boundaries, buffered messages surviving run replacement, queue messages routed through wrong semantics.
- **Use framework utilities, not raw path/fs**: Example: reviewer flagged hardcoded path, should use the framework's state directory resolver.

## Maintainer Review Styles

### Maintainer A (architecture-focused)
- Rewrites contributor approaches when he sees a better architecture (not rejection -- it's a compliment)
- Prefers ordered arrays over nested conditionals
- Traces root cause deeply -- will reject symptom-level fixes
- Patches branches directly to fix deeper correctness issues contributors missed

### Maintainer B (invariant-focused)
- Focuses on data structure invariants and semantic contract preservation
- Requires changelog fragment for user-visible behavior changes
- Will reject if compaction boundaries, lifecycle guarantees, or turn semantics are broken

### Maintainer C (evidence-focused)
- Requires visual evidence / screenshots for UI changes
- Will close docs/UI PRs without screenshots

### Maintainer D (prior-art-focused)
- Checks for prior art -- flags contributors who ignore existing PRs for same issue
- Flags blast radius issues -- especially when a fix affects broader scope than stated
- Verifies factual accuracy of constants (model limits, API specs)

## Bot Behavior (detailed)

### Primary reviewer bot
- Always posts substantive summary (never empty)
- Deep codebase awareness: cross-references patterns across entire repo
- Confidence score 1-5 with explicit "safe to merge" / "not safe to merge" verdict
- **Score -> merge probability**: 5/5 = trivial. 4/5 = good. 3/5 = concerns, may still merge. 2/5 = significant issues. 1/5 = critical bugs -- effectively a death sentence.
- Severity badges: P1 (real bugs) and P2 (concerns)

### Deep analysis bot -- deeper but inconsistent
- Often posts empty boilerplate with zero findings
- When substantive: traces call-chain impact that primary reviewer misses
- Re-reviews on EVERY push -- will raise same concern 3+ times. Reply gets progressively shorter.

### Security bot
- CWE classifications and severity ratings
- Findings are **informational, NOT blocking** -- maintainers routinely merge with open findings
- Do NOT treat as blockers. Acknowledge if straightforward; defer if complex.

### Hygiene bot
- Auto-closes for: dirty branch (too many files), >10 PRs from same author, stale
- No warning -- just closes. Can fire repeatedly.

## Gold Standard Examples

### Bot iteration: 5 rounds, merged
Exemplary external contributor bot interaction:
1. Primary bot found 3 issues -> author fixed all
2. Deep bot found 2 new P1s -> author redesigned
3. Deep bot found P1 + P2 -> fixed + added 5 tests
4. Deep bot found P2 -> author restructured
5. Primary bot confirmed: "Excellent work -- all three fixes are correctly implemented."

### CI triage: merged with failing CI
Author posted detailed triage -> maintainer merged despite red CI:
```
CI failure in `checks (node, test, 1, 2)` is unrelated to this PR:
- Failed test: unrelated module test
- Our changes: exclusively in `extensions/telegram/`
- Extension-specific checks all pass
- Same test also fails on main's latest CI run
```

### Fast merge: ~13 hours
Concise ping format worked:
```
@maintainer -- [one-line problem] -> [one-line fix]. [N] files, +X/-Y. Closes #XXXX.
```

## Label Taxonomy
- `too-many-prs` -- bot auto-close, PR limit exceeded
- `dirty` -- bot auto-close, unrelated changes
- `stale` -- bot auto-close, inactivity
- `superseded` -- replaced by newer PR
- `not-planned` -- maintainer deliberate rejection (don't reattempt)
- `already-fixed` -- resolved upstream
- `dedupe:parent` / `dedupe:child` -- bot deduplication (canonical PR vs copies)

## Code Style
- Files under ~700 LOC
- Subsystem-scoped logging
- Types exported alongside implementation (colocated)
- No `@ts-nocheck`, `@ts-ignore`, `any`
- No prototype mutation
- Changelog fragment for user-visible behavior changes

## Testing Patterns
- Test file exists for every changed source file (`*.test.ts` colocated)
- Use `vi.hoisted()` for mock variable definitions
- Use `beforeEach()` for cleanup/reset
- Edge cases: network errors, timeouts, empty inputs, boundary values
- Before/after evidence pattern (failing test before fix, passing after)
- Use `vi.mock("module")` not manual stubs

## Live Verification
Playwright MCP + live dev server at `localhost:18789`. After `pnpm test` passes, use Playwright to capture UI evidence for the PR description's Evidence section.

## Lessons Learned
- Main CI is frequently red (high merge volume). Don't rebase repeatedly -- post triage comment and wait.
- Bot-generated issues inflate linked issue counts. Filter by real users before claiming urgency.
- Competition check on issue number alone is insufficient -- search by function/filename too. Made this mistake TWICE.
- Maintainers sometimes rewrite your approach and merge under a new PR -- this is a compliment, not rejection.
- CI triage comments dramatically increase merge probability -- explain which jobs passed, why failures are unrelated, offer to rebase.
- Generated files must be regenerated after rebase if config files changed -- caused CI failure.
- Deep analysis bot raises same P2 concern across 3+ pushes. First reply: substantive. Second: "see prior reply." Third: "same as above."
- For UI fixes that process server data, trace BOTH sides (server -> wire -> UI) before choosing fix point.
- `gh run list --branch main` returns ALL workflows (not just CI). Small workflows are always green and give false "main recovered" signal.
- Ping earlier. One PR waited 4 days before pinging but was ready on day 1. Maintainer responded in 2.5h and merged in 39min.
- Some maintainers silent-merge clean small PRs -- no review comment, just direct merge after batch-reviewing.
