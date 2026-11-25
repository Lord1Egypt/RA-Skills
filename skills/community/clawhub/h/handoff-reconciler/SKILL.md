---
name: handoff-reconciler
description: Freeze a structured, machine-checkable handoff at the end of an AI coding session, then verify it at the start of the next session instead of trusting the summary — HEAD moved, branch changed, files claimed finished but edited since, next-action targets deleted or changed, verify command status. Use when asked to hand off a session, freeze a handoff, resume from a previous agent's handoff, check what drifted between sessions, or verify a handoff file (.handoff/HANDOFF.md). Not for general git status or diff inspection, for project management, or for scanning AI-agent skills (use skillscan).
license: MIT
compatibility: Requires Python 3.9+, pip, and git. Fully offline and deterministic; no LLM inside the tool.
---

# Handoff Reconciler

## What this tool does

Handoff Reconciler turns an agent's end-of-session summary into claims
that can be checked. `freeze` validates a draft handoff and fills in
the git ground truth itself — branch, HEAD, dirty files, and a sha256
content hash of every claimed file. `resume-check` then reconciles the
frozen claims against the repo as it is now and prints a traffic-light
drift report plus a corrected resume pack: what is still true, what
drifted, and which next actions survive.

## Install

```bash
pip install git+https://github.com/RakTikoo/handoff-reconciler
# or, isolated, with pipx:
pipx install git+https://github.com/RakTikoo/handoff-reconciler
```

With uv:

```bash
uv tool install git+https://github.com/RakTikoo/handoff-reconciler
```

This provides the `handoff-reconciler` command (standard library only).

## Run

At the end of a session, write a draft handoff as JSON (goal, tasks
with statuses, files claimed finished, next actions with target files,
a verify command — the format and an example draft are in the repo's
README and `examples/draft.json`), then freeze it:

```bash
handoff-reconciler freeze --draft draft.json
```

At the start of the next session, before trusting the summary:

```bash
handoff-reconciler resume-check
```

`handoff-reconciler show` prints a one-screen summary of the frozen
handoff. Add `--repo PATH` to work on a repo you are not standing in.

## Reading the results

Each claim gets one line: `[MATCH]`, `[DRIFT]` (changed, but usable
with care), `[BROKEN]` (the claim is false — a target file is gone, a
verify command failed), or `[NOT-RUN]` for the verify command. The
report ends with `OVERALL: MATCH`, `DRIFT` or `BROKEN`, and the
corrected resume pack.

Exit codes for `resume-check`: `0` — every claim MATCHes (the verify
command is MATCH or explicitly NOT-RUN). `1` — DRIFT present, nothing
BROKEN. `2` — a BROKEN claim, or a tool error (no handoff, malformed
handoff, not a git repo). For `freeze` and `show`: `0` is ok, `2` is a
validation or tool error.

The handoff's verify command is **never run by default** — it is
untrusted data from the file, reported NOT-RUN. It runs only with the
explicit `--run-verify` flag; use that only on handoffs you froze
yourself or have read first. When it runs, it has a timeout:
`--verify-timeout N` in seconds (default 120, must be 1..3600 —
outside that range is a usage error, exit 2).

## Limits

- Only the latest `.handoff/HANDOFF.md` is reconciled — no handoff
  chains yet.
- No transcript parsing and no automatic handoff writing: the agent
  writes the draft; the tool validates and verifies it.
- No signing in this version: integrity rests on the handoff living in
  git history plus the frozen content hashes. Anyone who can rewrite
  both the handoff and the repo history can forge a baseline.
- `resume-check` is read-only and never writes to the repo.
