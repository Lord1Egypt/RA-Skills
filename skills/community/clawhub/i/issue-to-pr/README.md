# 🔧 issue-to-pr

[![Skills.sh](https://img.shields.io/badge/skills.sh-issue--to--pr-blue)](https://skills.sh/4yDX3906/issue-to-pr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI Agent Skill that fixes a GitHub issue the way a maintainer would: **preflight the repository, reproduce the bug, prove the fix, then open a PR with evidence** — not just "generate a diff and hope".

---

## ⚡ Quick Install

```bash
npx skills add 4yDX3906/issue-to-pr
```

Or with the bundled installer:

```bash
git clone https://github.com/4yDX3906/issue-to-pr.git
cd issue-to-pr
bash scripts/install.sh --list-targets   # optional: see detected harnesses
bash scripts/install.sh
```

The installer auto-detects `~/.claude/skills`, `~/.qoder/skills`, and falls back to `~/.config/agent/skills`. Use `--target <dir>` or `--project` to control it.

> **That's it.** Give your agent an issue URL and watch it work.

---

## ✨ What changed in 1.4

The 1.3 workflow was a linear prompt: parse → fetch → clone → fix → test → PR. It worked when the issue was simple and the repository was conventional. It broke down on monorepos, stale environments, and untrusted issue text.

1.4 adds the parts a real fix needs:

- **Phase 0 preflight** — read `AGENTS.md` / `CONTRIBUTING.md` first, detect the package manager and task graph, check issue state, assignees, and existing PRs.
- **Reproduce before fixing** — a failing test (or a minimal script) that fails for the reported reason.
- **Baseline and red-green evidence** — record the pre-change test result, and prove the new test fails without the fix.
- **Blast-radius limits** — 10 files / 400 lines by default, no new dependencies, no CI or auth changes without approval.
- **State and resume** — `.issue-to-pr/state.json` lets an interrupted run continue instead of starting over.
- **Untrusted input policy** — issue bodies and comments are data, never instructions.
- **Self-review phase** — boundary cases, error paths, test validity, secrets, docs.
- **Repository conventions** — commitlint scopes, DCO sign-off, changesets, PR templates.
- **CI loop** — watch checks, read failing logs, iterate at most twice, never claim green when nothing ran.

---

## 🚀 Usage

In your agent, provide an issue reference:

```
/fix-issue https://github.com/owner/repo/issues/123
```

Or describe it naturally:

```
Fix web-infra-dev/midscene#3411 and open a PR.
```

Optional intents:

| Flag | Effect |
| --- | --- |
| `--dry-run` | Preflight, reproduce, and plan only. No branch, commit, push, or PR. |
| `--no-push` | Implement and verify locally, then stop before push. |
| `--draft` | Open the PR as a draft. |
| `--non-interactive` | Never block on a question; use safe defaults and record them. |
| `--max-files N` / `--max-lines N` | Override the blast-radius limits. |
| `--base <branch>` | Target a branch other than the default. |

---

## 🧭 Workflow

| Phase | What happens | Output |
| --- | --- | --- |
| **0. Preflight** | Parse the issue, read repository rules, detect stack, check for existing work, apply scope gate | `state.json`, blockers |
| **1. Reproduce** | Install without a full build, record the baseline, write a failing test | baseline log, failing test |
| **2. Plan** | Root cause, affected files, fix strategy, risk, out-of-scope list | plan in state |
| **3. Implement** | Minimal diff, repository style, tests and docs together | working tree |
| **4. Verify** | Focused test, red-green proof, package tests, types, lint, full suite compared to baseline | evidence artifacts |
| **5. Self-review** | Boundary cases, error paths, test validity, secrets, translations | review notes |
| **6. Commit** | Commitlint scopes, DCO, changesets, secret scan | commit |
| **7. Pull request** | Repository template, evidence body, draft policy | PR URL |
| **8. CI loop** | Check status, failing logs, at most two repair attempts | updated PR |
| **9. Report** | PR link, evidence, gaps, risk, next action | final report |

The full instructions live in [`SKILL.md`](./SKILL.md). The state schema is in [`references/state.schema.json`](./references/state.schema.json), and the PR evidence template in [`references/pr-evidence.md`](./references/pr-evidence.md).

---

## 🔒 Safety

- **Issue text is untrusted.** Commands, links, and instructions inside an issue are never executed.
- **No secrets.** The skill never reads `~/.ssh`, `~/.aws`, `~/.config/gh`, `.env`, or keychains, and scans staged changes before committing.
- **No force-push, no upstream push.** Work happens on your fork or your own branch.
- **Bounded changes.** Large fixes stop for approval instead of silently refactoring.
- **Local first.** Analysis and edits run on your machine; only standard Git and GitHub operations leave it.
- **No stored credentials.** It uses your existing `gh` session, or `GH_TOKEN` from the environment. If a token is used, the report reminds you to revoke or rotate it.

---

## 🖥️ Supported harnesses

The skill is harness-neutral: it describes capabilities, not IDE-specific tool names.

- **Claude Code and compatible harnesses** — auto-detected at `~/.claude/skills`.
- **Qoder** — auto-detected at `~/.qoder/skills`.
- **Generic agents** — installed to `~/.config/agent/skills`, or any directory via `--target`.
- **Cursor / Copilot / Windsurf** — load `SKILL.md` as a rule or project instruction; there is no universal skills directory yet.

---

## ⚠️ When not to use it

- Documentation or translation only — use a small docs PR instead.
- Dependency upgrades, migrations, large refactors, public API changes — need design approval first.
- Issues without a reproduction — investigate, but do not guess a fix.
- Issues already fixed or covered by an open PR — the skill reports the existing work instead.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a branch (`git checkout -b feature/improvement`).
3. Commit with a Conventional Commit message.
4. Open a PR describing the behavior change and how you verified it.

---

## 📄 License

MIT — see [LICENSE](LICENSE).
