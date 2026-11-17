# Running this skill on an agent that is not Claude Code

Read this when the host is codex, a Chinese coding agent, or anything else whose
tool names are not Claude Code's.

## What already works, unchanged

**The entire enforcement layer.** All of `scripts/` is plain Python — standard
library plus `PyYAML`, `python-docx` and `PyMuPDF` (painted PDF glyph inspection) — and every gate is a CLI
that exits 0/1/2 and appends a receipt. Verified by running them with no agent in
the loop, on the prepared Python 3.10+ runtime (`references/agent-setup.md`). So the
gates, the journal, the receipts, the renderers, the coverage counts and the
prediction lint behave identically on any host with that runtime. That is the half of this skill that stops it inventing
things, and it is not Claude-specific in any way.

**The judge and assessor prompts.** `agents/*.md` are self-contained personas —
"You are a literal applicant-tracking-system parser…" — with no reference to how
they were dispatched. Any mechanism that gives one of them a fresh context works.

**The mode files, the references and the market tables.** Prose and data.

So what needs translating is small and specific: **how you ask the user a
question, and how you open a fresh context.** Three affordances, below.

## 1. Asking the user — `AskUserQuestion` is a shape, not a requirement

`modes/apply.md` Step 0 and the hand-off step name Claude Code's
`AskUserQuestion`. What the skill actually requires is the SHAPE: a small number
of questions, asked in **one** message, each with concrete options rather than an
open prompt.

On a host without it, ask the same questions as a numbered list in a single
message, with the options spelled out as lettered choices. Do not degrade to one
question per turn — the reason the skill asks for a single call is that a
four-round interrogation before any work is what makes people abandon the run.

The host's actual question tool, capacity and interaction rules take precedence
over this example. Ask only what is still missing; a current user answer remains
valid across mode changes for the same target. Never invent an unavailable tool.

**Measured, and it is not only an other-agent problem.** Ten of the fifteen
`with_skill` runs in the source repository's iteration-2 evaluation recorded
`AskUserQuestion` as unavailable — those were Claude Code subagents, which do not
get the tool either. Any run without an interactive human is in the same
position: state the assumptions you proceeded on instead, and carry them into the
completion message so the user can correct them.

## 2. Fresh contexts for the judges — the one that actually matters

The three-judge review loop and the two mock assessors are called
non-negotiable, and their value is **information isolation**: each judge sees the
artifact and its own persona file, and nothing else. A judge that watched the
tailoring happen is not a second opinion, it is the same opinion.

Any of these gives you that, in preference order:

1. **A subagent / task / sub-session tool**, if the host has one. Dispatch all
   three at once so they cannot influence each other's ordering.
2. **A fresh invocation of the host's own CLI**, which is what makes this
   portable. The persona files are standalone, so:

   ```bash
   codex exec "$(cat agents/ats-screener.md)

   POSTING:
   $(cat "$WS/posting.yaml")

   CV:
   $(cat "$WS/cv.md")

   CV LANGUAGE: en" > "$WS/judge-ats.md"
   ```

   Substitute the host's equivalent (`claude -p`, `gemini -p`, and so on). One
   process per judge, run them concurrently, and save each verdict to a file so
   `parse_verdicts.py` can read it.

   **Measured end to end, 2026-09-06, codex-cli 0.147.0.** All three judge
   personas were run through `codex exec` against a real apply workspace from
   the iteration-2 eval — `posting.yaml` and `cv.md` for a US ICU nursing role.
   Each returned a well-formed block with a single `VERDICT:` line, and the
   skill's own `scripts/parse_verdicts.py` accepted all three, exited 0, wrote
   its receipt and recorded `combined_verdict: PASS`. So this is a verified
   path, not a plausible one. `gemini` and `cursor-agent` were present on the
   same machine and were NOT tested; nothing here claims they work.
3. **A separate chat session** the user opens and pastes into. Slow, and it works.

**If the host has none of these, say so — do not simulate the judges in the
conversation that wrote the CV.** A judge in the same context has read the
tailoring plan, the gap analysis and every reason the CV says what it says; its
PASS carries none of the information a real second opinion carries. Running it
anyway and reporting three PASSes would be the exact failure this skill spends
most of its design avoiding: an output that looks reviewed and was not.

If no fresh context is available, preserve the draft and report that independent
review is incomplete. You may inspect it yourself for obvious defects, but do
not create judge verdict files, manufacture review receipts or label it reviewed.
Resume the independent review when a supported mechanism becomes available.
`parse_verdicts.py` checks verdict syntax, not context isolation; a parseable
block alone is never evidence that an independent review happened.

## 3. Fetching a posting or a paper

`WebFetch` and `WebSearch` are named throughout for posting retrieval and for
enriching a profile from the candidate's own papers and repositories. Use the
host's equivalent. If it has none, the skill's existing terminal case already
covers it and needs no translation: **ask the user to paste the posting text**,
and ask them for the specific facts a paywalled paper would have supplied. That
path is already the correct behaviour on a blocked fetch, so a host with no
fetch tool is on a supported road, not an unsupported one.

`opencli` in discover mode is a separate binary and works anywhere it is
installed; `scripts/doctor.py` reports its absence and what that costs.

## 4. Where the skill and the profile store live

Skill discovery differs per host — `~/.claude/skills/`, `~/.codex/skills/`, and
others. Install however that host expects; nothing in the skill reads its own
install path except through `scripts/paths.py`, which derives it from the script
file's location.

The profile store is `~/.claude/job-profiles/` by default, and **that default is
kept even on other hosts on purpose**: a user who runs this skill from two agents
should get one set of CVs, not two half-populated ones. Set
`JOBHUNT_PROFILES_ROOT` to move it if the default is wrong for the machine — an
unwritable home, or a deliberate split.

## 5. What to check before trusting a run on a new host

The agent prepares missing dependencies and daily-browser CDP using
[agent-setup.md](agent-setup.md), then runs the capability checks below.

```bash
python3 scripts/doctor.py          # capabilities, and what each missing one costs
```

On a checkout of the source repository (https://github.com/addsumtech/job-hunt), `python3 -m pytest scripts/tests/ -q`
also runs the enforcement layer on this machine. That test suite is the real portability check: it exercises every gate against
fixtures and needs no agent at all. A host where it passes can run the gates; a
host where it fails has a Python or dependency problem, not a skill problem.

### Optional audit of this machine

The test suite checks supported copy and symlink installations in temporary directories. To audit the actual installed skill against a checkout of the source repository, run `JOBHUNT_CHECK_INSTALL=1 python -m pytest scripts/tests/test_install.py -q` in that checkout. Only a machine that migrated from `job-application` should additionally set `JOBHUNT_CHECK_MIGRATION_ARCHIVE=1`; a fresh installation has no legacy archive to preserve. These checks never create or change the user's runtime skill directories.

## Saving a master

**One candidate has one CV per language, and saving a new one never overwrites another language's.** A Chinese CV is a different document from an English one — different conventions, length rules and personal-data expectations — not a translation of it, so a user who supplies both has two masters: `profile.yaml` and `profile.<lang>.yaml` beside it. **Save through `python3 scripts/save_profile.py --name <name> --profile <file>`, never by writing the path yourself.** It resolves the slot by reading each existing master's own `meta.language` rather than trusting a filename, so a second English CV goes back into the legacy `profile.yaml` instead of becoming a duplicate; it backs up what it replaces; and it refuses a profile with no `meta.language`, because the unsuffixed slot is where a legacy English master usually lives and dropping an untagged CV there is the overwrite this is here to prevent. On the read side the same rule runs backwards: tailor from the master whose language matches the CV language chosen in Step 0, and say which file you took as the base. Reaching for the English master to build a Chinese CV throws away the one the user wrote for exactly that purpose.

