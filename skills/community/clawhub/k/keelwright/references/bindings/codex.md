# keelwright binding — Codex

Codex (OpenAI) runs agents via `codex` CLI / `~/.codex/AGENTS.md`. Wire keelwright's gates
the same way as any runtime.

## Setup (runtime-neutral)
- Add a project `AGENTS.md` (or `~/.codex/AGENTS.md`) that loads keelwright's gate checklist
  from `references/security-gates.md` and the loop phases from `references/phases.md`.
- Web Guard auto-injection is Hermes-only; on Codex add a pre-tool rule that runs
  `scripts/detect_guard.py` and surfaces the verdict.

## Commands (replace with your stack)
- test / lint / build / quality: your project's CLI.

## Web Guard
- Before ANY web fetch: `python <keelwright>/scripts/detect_guard.py`
- If not ACTIVE, tell the user before proceeding.
- Heuristic backstop: `python <keelwright>/scripts/web_heuristic_guard.py --text "..."`

keelwright is MIT-0. This binding is instructions only.
