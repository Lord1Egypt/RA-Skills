# GitHub Repo Creation Guardrails

## Default Privacy Policy

**ALL new repos default to PRIVATE.** Only make a repo public if <operator> explicitly asks.

**NEVER change the privacy of existing repos** unless <operator> explicitly instructs. Even when updating, syncing, or fixing a skill — leave repo visibility exactly as it is.

## Private-Only Repos

These repos MUST always be private. If any need to be made public, <operator> will say so explicitly:

- ocas-vibes
- ocas-vpn (and any VPN-related repo)
- ocas-dispatch
- ocas-haiku
- voice-call (and any telephony repos)
- ocas-bones
- indigo-repo (and any repo containing personal/identity data)
- headhunter (and any job-search repos)
- ocas-inception
- ocas-thread

Everything else defaults to private on creation but CAN be made public by asking.

## Repo Creation Guardrail Checklist

Before creating ANY GitHub repo, verify:

1. **Author check.** Read `metadata.author` from the skill's frontmatter. If the author is not `<agent-name>`, `<user>`, or `<agent-handle>`, **STOP.**
2. **OCAS prefix check.** Only skills with an `ocas-` prefix in `~/.hermes/skills/` get repos.
3. **Bundled skill check.** If the skill name matches a known hermes-agent built-in (`api-integration`, `google-workspace`, `deployment`, `docker-management`, `email-sending`, `git-operations`, `json-formatting`, `csv-parsing`, `database-operations`, `execute-code`, `unit-testing`, `web-extract`, `learn`, `terminal-run`, `title-sessions`, `voice-call`, `prism-*`, `reflexion-*`, `cek-*`), **STOP.**
4. **Duplicate check.** Run `gh repo list` first. If a repo with the same or similar name exists, use the existing one. Ask <operator> which to keep if ambiguous.
5. **Don't create repos for other people's skills.** When asked to fix/improve an existing skill on an existing platform (e.g., agentskill.sh), find the original repo and create PRs there. Do NOT create a new GitHub repo for someone else's skill.

If any check stops you, log the decision in `decisions.jsonl` with `decision_type: "repo_creation_blocked"` and tell <operator> why.

## PR Workflow

- **One PR per distinct issue.** Don't bundle unrelated fixes into a single PR.
- **Match scope to request.** When asked to fix one thing, fix that one thing. Don't also refactor unrelated sections.
- **Find the original repo first.** For skills on agentskill.sh or other platforms, find the source repo via the "Source" link on the skill page. Fork that repo, create a branch per issue, and PR upstream.