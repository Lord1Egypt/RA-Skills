# Open-Sourcing a Skill — Full Playbook (clawhub / GitHub / skills.sh)

> Scope: OpenClaw / Claude Code / Cursor / any AI-Agent skill ecosystem.
> Goal: safely open-source a local (often internally-coupled) skill to public hubs.
> This playbook is the distilled, vendor-neutral methodology behind this skill's
> 10-step workflow — read it once before your first open-source, and skim the
> matching section whenever a step feels ambiguous.

---

## 0. Slug collision pre-check (ALWAYS step 1)

**After picking a slug, the very first action must be a name-collision check.
Never build the fork first and discover the clash later.**

```bash
clawhub inspect <slug>
# no hit  = safe to use
# hit     = STOP, let the user decide: rename or coexist
```

### Handling a collision

| Situation | Action |
| --- | --- |
| Same owner, same name | Just bump the version and publish |
| Different owner, same name | **Must rename** (add a brand prefix, or adjust naming) — don't fight for it |
| Different name but concept overlaps heavily | Have the user read the other SKILL.md and pick a differentiated angle, then rename |

### Why

A real project once collided with an already-registered name and wasted 80+ minutes
of fork rework. clawhub does **not** support slug rename — once published it's locked.

---

## 1. Decision framework (4 questions before starting)

| Question | Criterion |
| --- | --- |
| Should this skill be open-sourced at all? | Heavy internal coupling ≠ "can't open-source" — trigger a "remake" mindset. Is the core capability generally useful in public? |
| Evolve the original vs. strip into a fork? | Internal users still depend on it / internal behavior can't change → **fork**. Only a few internal details → evolve the original |
| Fork from the released stable version or current HEAD? | The released stable version (more controllable) — never fork from a dirty WIP |
| Should the remake expand scope? | Fine to add — but add it in the fork; keep the internal version on its own cadence |

---

## 2. Fork directory policy (hard rule)

```plaintext
<workspace>/
├── skills/<name>/                 ← internal version, keeps its own release cadence
└── opensourceskills/<name>/       ← open-source fork, evolves independently
```

- The fork and internal version have **independent commits, version numbers, sign.key**
- Keep the fork under `opensourceskills/` (make sure the workspace .gitignore does NOT ignore it)
- **First public version starts at 1.0.0** — don't carry over the internal version number
  (the clawhub package is a first release)

---

## 3. Fork strip checklist (11 hard rules)

### Must delete / must change

| # | Item | Action |
| --- | --- | --- |
| 1 | sign.key, skill-meta / agent-generated `*.json.md` | Delete — internal signatures / agent artifacts |
| 2 | `.install-source.json` | Delete — internal install-source marker |
| 3 | `__pycache__/`, `*.pyc`, `.skill-data/` | Delete — runtime cache left by agent runs |
| 4 | `USAGE.md` (if it duplicates SKILL.md) | Delete — avoid bilingual maintenance cost |
| 5 | Hardcoded internal hosts | Change to runtime concatenation or env vars |
| 6 | Hardcoded internal paths | Change to `pwd`, user args, or env vars |
| 7 | Internal concept references (company/platform names) | Change to generic names (`PROJECT_NAME`, `<your-tool>`) |
| 8 | Internal email examples | Replace with `user@example.com` |
| 9 | Internal gitignore artifact paths | Delete; use generic `id_rsa`, `*.p12`, `certs/*.key` |
| 10 | Internal names / aliases / UIDs | Delete; use one consistent public identity |
| 11 | Business-system fallbacks (env/region/namespace) | Don't keep; make them a user-configurable list (e.g. `--probe-env "A,B,C"`) |

### Zero-internal-info verification (run before commit)

```bash
# Feed your company's internal keywords here (see the configurable keyword list)
grep -rE '<internal-keyword-1>|<internal-keyword-2>|...' opensourceskills/<name>/
```

Expected: only the public author identity is whitelisted; everything else = zero hits.
(Public product/brand names that are already public may be intentionally kept.)

---

## 4. SKILL.md metadata (required for open-source)

### 4.1 frontmatter (only 2 fields)

```yaml
---
name: <slug>
description: >
  English body (clear trigger conditions + non-trigger conditions).
  Append Chinese/other-language trigger phrases after the English body.
---
```

⚠️ **3 cross-agent frontmatter constraints:**

1. Use `>` folded scalar for `description` (avoids quote-escaping issues)
2. `description` ≤ 1024 bytes (Anthropic limit)
3. frontmatter keeps **only name + description** — move version / metadata / author /
   tags into the Markdown body, otherwise strict YAML parsers (e.g. Qoder) report
   "Invalid SKILL.md format" (proven across real releases).

### 4.2 SKILL.md body top 4 lines (required, right after the `#` title + intro paragraph)

```markdown
- **Version**: 1.0.0
- **License**: MIT
- **Author**: <Public Name> · [github.com/<handle>](https://github.com/<handle>)
- **Repository**: https://github.com/<handle>/<repo-name>
```

⚠️ clawhub cards parse **only the top of SKILL.md** — no matter how nice the README is,
it doesn't count for the card (proven in practice).

### 4.3 description i18n template

English body + trigger-phrase block for other languages appended — balances
international matching with non-English agent triggering.

---

## 5. Directory structure standard (open-source fork)

```plaintext
opensourceskills/<name>/
├── SKILL.md           ← top has Version / License / Author / Repository (4 lines)
├── README.md          ← detailed docs (user's view) + Changelog
├── LICENSE            ← MIT (must be user-decided)
├── scripts/           ← executables, prefer bash (fewer cross-platform deps)
├── references/        ← optional, supplementary docs (progressive disclosure)
└── .gitignore         ← generic safety rules
```

`tmp/`, `output/`, `tests/`, `.cache/` etc. do **NOT** go into the fork (local-only).

---

## 6. CLI design principles (essential for open-sourcing)

| Principle | Rationale |
| --- | --- |
| CLI flag + env var dual-track | e.g. `--workdir` / `<TOOL>_WORKDIR` / `pwd` three-tier priority |
| env var names carry a skill prefix | e.g. `<TOOL>_*` — avoid polluting the user's environment |
| Business-configurable lists are not hardcoded | `--probe-env "A,B,C"` user-defined, default to generic values |
| Advanced capabilities are opt-in | Default off; print a hint to add a `--force-*` flag when unavailable |
| `--help` covers every flag | A UGLIC must-check item |
| **locale detection over hardcoded language** | `--lang/--locale` defaults from `$LC_ALL/$LC_MESSAGES/$LANG`, never hardcode |

### 6.1 User-authorization flags (hard rule)

`--i-am-sure` / `--force` / `--yes` and similar authorization firewalls must
**NOT be added by the AI on its own — the user must confirm in text**.
Piping `echo y |` as an equivalent bypass is equally forbidden (proven violations exist).

---

## 7. Cross-platform fallbacks (depth by audience)

⚠️ **Not always all of them**: if the skill is explicitly "Linux only", skip macOS
realpath/sed fallbacks; **if it might run on macOS / Windows Git Bash, they're mandatory.**

| Command | Fallback |
| --- | --- |
| `realpath` | Not on macOS BSD — use `cd && pwd` |
| `readlink -f` | Not on macOS — try `command -v greadlink` first |
| `sed -i` | macOS needs `sed -i ''` — try `command -v gsed` |
| `numfmt` / `stat -c` | Not on macOS — probe with `command -v` first |
| `mapfile` | Not in macOS bash 3.2 — use a `while read` loop |
| cgroup / PVC | No `/sys` on Windows Git Bash — guard with an IS_WINDOWS check |

Standard bash header:

```bash
set -euo pipefail
command -v <tool> >/dev/null 2>&1 || { echo "Missing <tool>"; exit 1; }
```

---

## 8. Token hygiene (hard rule)

| Stage | Action |
| --- | --- |
| User pastes a token | **Your first reply must** remind: "since you pasted it, consider revoking it" |
| Passing a token to a CLI | Only via env var, `TOKEN=xxx command`; never write to file / git / memory |
| After publish | Remind again to revoke on the web |
| Token storage path | `<workspace>/.secrets/tokens.env` (chmod 600 + dir 700 + fully gitignored) |

### 8.1 Tokens are NOT shared across channels (key)

| Channel | Auth |
| --- | --- |
| **clawhub** | `CLAWHUB_TOKEN`, obtained via `clawhub login` web flow (fully independent system) |
| **GitHub** | Personal Access Token (PAT), **completely independent** from clawhub |
| **skills.sh** | No independent token — indexed via GitHub repo, sync uses the GitHub PAT |

⚠️ GitHub push over a restricted network uses an `Authorization: Basic base64(x-access-token:TOKEN)`
header injection, so the **token never enters the remote URL** (bearer is no longer accepted):

```bash
AUTH_B64=$(printf "x-access-token:%s" "$GITHUB_TOKEN" | base64 -w0)
git -c http.extraHeader="Authorization: Basic $AUTH_B64" push origin main
```

---

## 9. Three-channel release order

| # | Channel | Tool | Note |
| --- | --- | --- | --- |
| 1 | clawhub.com | `clawhub publish <abs-path>` | **Must use an absolute path** (relative path occasionally errors "SKILL.md required") |
| 2 | GitHub | `git init -b main` + push | Occasional 502 on restricted networks — retry 3-5 times in a loop |
| 3 | skills.sh | auto-synced via the GitHub repo | Only visible in `npx skills list` after ~24h |

### 9.1 clawhub known behaviors

- Forces LICENSE to MIT-0 (local LICENSE file is ignored; cross-channel license
  mismatch is a platform behavior, not a bug)
- No visibility parameter — use hide/unhide to control visibility
- Occasional rate limit — `sleep 30` and retry

### 9.2 GitHub push retry template

```bash
AUTH_B64=$(printf "x-access-token:%s" "$GITHUB_TOKEN" | base64 -w0)
for i in 1 2 3 4 5; do
  timeout 150 git -c http.extraHeader="Authorization: Basic $AUTH_B64" push origin main && break
  sleep 8
done
```

### 9.3 Push verification (critical)

`git push` exiting 0 does **not** guarantee the commit reached the remote (network
jitter / timeout wrapper / 502-then-kill can all exit 0 with the remote unchanged).
Verify by comparing local HEAD to the remote sha:

```bash
LOCAL=$(git rev-parse HEAD)
# Prefer GitHub API (more jitter-resistant), fall back to ls-remote
REMOTE=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/<handle>/<repo>/commits/main" | grep -m1 '"sha"' | ...)
[ "$LOCAL" = "$REMOTE" ] && echo "verified" || echo "push NOT effective"
```

### 9.4 Order principle

Release one channel, **wait for its scan to pass + actually test-install it**, then
release the next. Don't batch-push everything at once.

---

## 10. New standalone GitHub repo essentials

First commit into a brand-new repo must start with:

```bash
cd <repo-path>
git config user.name "<Public Name>"
git config user.email "<handle>@users.noreply.github.com"
git init -b main            # default branch main
git symbolic-ref HEAD refs/heads/main   # old-git fallback
```

### Why

**Containers often have no default git user.name/email** — commit fails outright with
"empty ident name". A real first-release once hit this while creating a new repo.

### LICENSE must be user-decided

Never fill a fake name / placeholder contributor: the user must choose
**MIT / Apache 2.0 / GPL** + **real-name attribution**. Use the public identity, not an internal email.

---

## 11. UGLIC five-dimension check (run before release)

GLIC = G / L / I / C = **4 dimensions** (internal quality)
UGLIC = U + G + L + I + C = **5 dimensions** (adds a user-experience dimension)

| Dimension | Focus |
| --- | --- |
| **U (User Experience)** | UGLIC-only. Is the whole path (README → trigger → install → run) smooth? Does `--help` cover every flag? Do error messages give a clear next step? SKILL.md length (>500 WARN / >800 ERR) |
| G (Grammar / conventions) | frontmatter field discipline, Python `ast.parse`, JSON validation, Markdown rendering |
| L (Logic) | reachable control flow, boundary conditions, error-recovery paths, loop invariants |
| I (Integrity) | every script / config / section referenced by SKILL.md exists; cross-section references intact; no build-artifact residue |
| C (Containment / credentials) | grep for tokens / keys / internal domains / internal emails — all zero hits |

The UGLIC report must be **0 ERR**; every WARN either fixed or explained before shipping.

### 11.1 Self-audit + three-tier samples (for audit/check-type skills)

After release, self-check and run simple / medium / complex real samples, and for
each finding ask:

- "Which rule did I derive this from?" → find the rule
- "Can't find a rule?" → on what basis did I flag it? (external memory / generalization)
- "Does it recur?" → does it deserve a dedicated check item

Findings flagged from memory / generalization = **rule blind spots** → promote to a
sub-check next version. **Reporting blind spots is more valuable than reporting coverage.**

### 11.2 Cross-check two audit tools (before release)

Don't run only UGLIC — also run a generic release audit and a hub-specific audit.
The two toolsets have complementary blind spots; running just one always misses something.

---

## 12. Restricted / sensitive publishing environments

Some internal hubs mark certain users/departments as "restricted", blocking public
visibility (often via a silent downgrade to private).

- ⛔ Do NOT self-decide to add `--visibility private` as a workaround — once an existing
  skill is downgraded, even a `PUT edit` may not restore it; you'd need an admin
- ✅ Correct approach: omit the visibility flag so the release tool refills the hub's current value
- ✅ Public channels (clawhub / GitHub / skills.sh) are **not** subject to this restriction

### Verification rule

After a publish/edit that changes visibility / displayName / summary, **do not trust
the response fields** — re-GET the detail endpoint (and a `PUT edit` empty-body probe)
to confirm the actual persisted value.

---

## 13. Common anti-patterns

| ❌ Anti-pattern | ✅ Correct |
| --- | --- |
| Editing the original while editing the fork | Original untouched; only edit the fork |
| Fork dir name with `-os` / `-opensource` suffix | Use `opensourceskills/<name>/`, slug matches the original |
| `v0.1` / `v0.x` trial releases | Go straight to `v1.0.0` (hub users expect a "mature" first release) |
| GitHub repo default branch `dev` / `master` | Must be `main` (old-git `git symbolic-ref HEAD refs/heads/main` fallback) |
| LICENSE with fake name / placeholder contributor | User-decided MIT / Apache + real-name attribution |
| Pasting raw internal grep output into chat | Sanitize any internal grep output first |
| frontmatter with version / metadata / author / tags | Only name + description (move the rest to the body) |
| Judging visibility publish success by response field | Second GET on the detail endpoint to verify |
| One commit spanning N things | One commit per thing; memory notes commit separately |

---

## 14. Suite-repo conventions

When a new standalone repo hosts a set of related skills:

### 14.1 Root README needs a stages roadmap table

```markdown
| Stage | Skill | Status | What it does |
|---|---|---|---|
| Creation | `skill-creator` | 🚧 Not yet released | Scaffold a new skill from intent |
| **Audit** | **`glic-check`** | ✅ **v1.0.1** | **Systematic quality review** |
| Release | `skill-release` | 🚧 Not yet released | Package + publish to hubs |
```

🚧 List placeholders too (coming soon), so users don't install a member that 404s.

### 14.2 Each skill has a "Part of \<suite\>" section

Present in both SKILL.md and README.md, pointing back to the repo + listing sibling
skills' current status (a condensed version of the root table).

### 14.3 Suite members release independently

Avoid the "table lists 5 but only 1 published" dead-end where installing a missing
member fails.

### 14.4 Incremental release into a mono-repo (never push the fork's main)

When the target repo is a **mono-repo** (root has `skills/`, several skills share one repo —
`build-better-skills` is itself one), do **not** run the normal push flow: it treats the fork as
the repo root and force-overwrites every sibling under `skills/`
(`better-office-work-flow` was wiped this way on 2026-08-02: 4 skills → 1). `github_push.sh`
detects this and exits 8. The correct path is an **incremental subdirectory release**:

```bash
SLUG=<skill-slug>
SRC=~/.workbuddy/skills/$SLUG/
REPO=~/skills/<repo-name>                        # reuse the standing clone, not a fresh /tmp one
rsync -a --delete "$SRC" "$REPO/skills/$SLUG/"   # --delete: leave no stale files behind
cd "$REPO" && git status --short                 # must show ONLY skills/$SLUG/**
git add "skills/$SLUG" && git commit -m "$SLUG v<x.y.z>: <one line>"
git push origin main
```

"First release of a new member" and "new version of an existing member" are the same path —
only the commit message differs. `--delete` matters: without it, files you removed at the source
never leave the repo, and the `git status` check stops being a trustworthy "only this member
changed" gate.

**Two network traps (verified 2026-10-06, mainland-China networks)**:

- `git push` hangs or fails because `github.com:443` is blocked — while `api.github.com` still
  works, which easily misreads as "network is fine". Push through the local proxy:
  `git -c http.proxy=http://127.0.0.1:<port> -c https.proxy=http://127.0.0.1:<port> push origin main`.
- `raw.githubusercontent.com` is blocked → verify through the GitHub **API** instead:
  `GET /repos/<owner>/<repo>/contents/skills/<slug>/SKILL.md?ref=main` (base64-decode, grep
  `**Version**`), plus `GET .../contents/skills/<slug>/scripts` to confirm new files actually shipped.

**If a repo was already overwritten**: recovery is usually possible via `git reflog`, or via the
**dangling commit** the force-push left on GitHub (that is how `better-office-work-flow` was
recovered from `63ae4858` on 2026-08-02). Stop pushing immediately — a further push can garbage-collect
the dangling commit.

---

## 15. Memory notes

After open-sourcing a skill, record:

```plaintext
memory/project_<slug>_opensource_fork.md
  - Decisions: why open-source, fork vs. evolve, how the first version number was chosen
  - Changes: CLI design, env var naming, cross-platform fallbacks
  - Lessons: the list of design questions the user decided
  - Links: point to the previous open-sourced skill's memory (chained continuity)
```

Promote general lessons into `feedback_*.md` notes.

---

## Quick checklist

```plaintext
□ §0  slug collision pre-check (clawhub inspect)
□ §1  answer the 4 decision questions
□ §2  fork path opensourceskills/<name>/
□ §3  11-rule strip checklist + zero internal-info grep
□ §4  frontmatter name+description only + 4 body metadata lines
□ §5  directory structure standard
□ §6  CLI dual-track + locale detection + no self-decided auth flags
□ §7  cross-platform fallbacks (depth by audience)
□ §8  token hygiene (env only + per-channel independent tokens)
□ §9  three-channel order + clawhub abs path + GitHub retry + push verify
□ §10 new repo git config + main branch + user-decided LICENSE
□ §11 UGLIC 5-dim + self-audit three-tier samples + cross audit tools
□ §12 restricted-env visibility not self-decided + detail verification
□ §13 avoid the anti-patterns
□ §14 suite repo stages table + Part-of section
□ §15 memory notes project_*.md + general feedback_*.md
```
