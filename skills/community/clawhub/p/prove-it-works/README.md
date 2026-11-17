# Prove It Works

**Free from ShipSnag.** Before your AI agent says "done", this runs your tests and build and shows the real output. If anything fails or breaks a project rule, the agent has to say so and fix it.

## Install (30 seconds)

Unzip into your agent's skills folder:

- Claude Code: `~/.claude/skills/prove-it-works/` (or `.claude/skills/` inside your project)
- Claude.ai: Settings > Capabilities > Skills > upload the zip
- Other agents that read SKILL.md files: their skills folder

Start a new session. Nothing else to install: the scripts use only Python's standard library and git.

## Use it

- **At the end of a task:** the agent runs it by itself before saying "done". You can also ask "prove it works", "did you run the tests?" or "run the checks". You get a first line with one of four verdicts, the real output of every check, and a finding for each problem with the file and line:
  - `PROVEN: all 3 checks passed, no problems in the change` (a task was given and everything ran)
  - `CHECKS PASS (task not verified): ...` (nothing failed, and the line says what was not covered)
  - `NOT VERIFIED: 2 checks could not run (...)` (for example dependencies not installed)
  - `NOT DONE: 1 failing check, 2 problems in the change`
- **After you correct a mistake:** say "don't do that again". The agent turns it into a rule in `.shipsnag/rules.md` (a pattern that must not appear, a folder that must not change, or a command that must pass), and every later proof checks it.

## What it checks

- **Your real commands:** package.json scripts (run with npm, pnpm, yarn or bun, whichever your lockfile says), Makefile targets, pyproject tasks, pytest or unittest, ruff, flake8, mypy, cargo, go, Maven, Gradle, Bundler, Composer, .NET and Deno, each with a timeout, a total time budget and no network installs. A check that could not run (dependencies not installed, tool missing) is marked NOT RUN, never passed and never failed. A test run whose output reports failures is a failure even if the command exits 0. Scripts named or doing deploy, release, publish, migrate or install are never run automatically.
- **The change itself:** on a feature branch, every commit since the default branch plus uncommitted work; otherwise your uncommitted work. It looks for focused or skipped tests, new test files your test command never picks up, deleted or loosened assertions, tests that cannot fail, snapshots and golden files re-recorded to match a bug, test commands and CI jobs changed so they cannot fail, lowered coverage thresholds, swallowed errors, special-cased test inputs, hardcoded results, files changed outside the task, task items such as a named function or `--flag` that no code implements, debug leftovers, secrets and `.env` files, unasked dependencies, lockfiles not updated, edited migrations and schema changes without one, TODOs, stubs and conflict markers, `@ts-ignore` / `eslint-disable` / `# type: ignore`, changed public function signatures, generated or large files, and screenshots or other binaries nothing uses. Minified, generated and vendored files are skipped by the line checks.
- **Your project rules:** CLAUDE.md, AGENTS.md, .cursorrules, .cursor/rules, .github/copilot-instructions.md, CONTRIBUTING.md and .windsurfrules. Rules a script can check (package manager, forbidden imports, files not to edit, required commands, file naming, "user-facing texts are a contract") become checks; the rest are listed for the agent to check by reading.

## Optional: run it automatically when Claude Code stops

Claude Code can run a command each time the agent finishes a turn (a **Stop hook**). This snippet makes the agent keep working while the proof says NOT DONE. It is **not installed for you**. Add it yourself to `.claude/settings.json` in your project, or to `~/.claude/settings.json` for every project, and adjust the path to where you unzipped the skill:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/prove-it-works/scripts/prove.py --hook --only tests,lint,typecheck,rules --timeout 240",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

How it behaves:
- It finds the project from `CLAUDE_PROJECT_DIR` (or the hook's working folder) and checks the whole git repository, even if the session moved into a subfolder. It does nothing outside git.
- It proves uncommitted work, commits on a feature branch, and commits made on the default branch during the session. It reads the task from the session transcript, so scope and task items are checked too.
- When the proof says NOT DONE, it prints `{"decision": "block", "reason": "..."}` with the failing checks and problems, which keeps Claude working on them. It blocks again only if the code changed since the last block. If Claude stops again without changing anything, the stop goes through and you get a message saying the work is still NOT DONE.
- It never blocks when checks could not run (dependencies not installed, no test command, a timeout): it tells you once with a message instead.
- It does not rerun anything when nothing changed since the last proof (for example after a question-only turn), and it stops its own commands within a total budget below the hook timeout. If Claude Code stops the hook, the test processes are stopped with it.
- It gives up blocking after 8 attempts on the same session and tells you.

Source: Anthropic, Claude Code hooks reference, https://code.claude.com/docs/en/hooks (checked 2026-10-14): the settings format (`"type": "command"` handlers with an optional `timeout`, default 600 seconds, and a hook that reaches its timeout has its output discarded), the common input fields (`session_id`, `transcript_path`, `cwd`), `CLAUDE_PROJECT_DIR`, Stop hooks receiving `stop_hook_active`, blocking with `decision: "block"` plus `reason`, and `systemMessage` as a message shown to the user. Hook formats change; check that page if the snippet stops working.

## What it doesn't do

- It never installs packages, never downloads anything, and never runs destructive commands (no `git checkout`, `reset`, `clean` or `rm`). Your project's own test and build commands run as they normally do; anything that looks like a deploy, release, publish, migration or install is listed as NOT RUN instead.
- It masks secrets in command output (key-shaped values, `password=...`-style pairs, Bearer tokens, and the values of secret-named environment variables) before showing it.
- It never edits your code. Fixes come from the agent, shown as normal changes.
- It can't see CI-only differences, flaky tests, or anything that needs a human or a browser. The report says so.

## Files it adds

Only in `.shipsnag/`: `rules.md` when you add a Never Twice rule, and with your OK one line per run in `ledger.md` (verdict and counts, never code or secrets). Delete or gitignore them any time.
