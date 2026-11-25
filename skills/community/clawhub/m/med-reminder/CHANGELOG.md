# Changelog

## Unreleased

### Security: ClawHub audit fixes

Fixes from the [ClawHub security audit](https://clawhub.ai/thegizmopro/skills/med-reminder/security-audit).
The semantic version bump happens at ClawHub publish time, not here.

- **Scoped, multi-state-safe Windows task cleanup.** `setup-tasks.py` migration
  now deletes only tasks matching the pre-PR3 per-dose naming scheme. Every
  state's `tick-<hash>` task is protected, whether found by registry or by
  name. Anything else in `\MedReminder\` is reported as
  `UNRECOGNIZED (untouched)` unless you pass `--purge-unknown`. `--clear`
  also spares other states' ticks by name, not only through their registry
  files.
- **POSIX test isolation.** The send-lease crash test now starts its child in
  a new session, so the `killpg` that kills it can never reach the pytest
  runner or an agent that invoked it.
- **`confirm --all` explicitness rule.** SKILL.md and `reply.py confirm --help`
  say the agent may use `--all` only when the user explicitly said they took
  all scheduled meds. Ambiguous or partial replies get a per-med confirm or a
  follow-up question.
- **Privacy disclosure.** The README says reminder messages (medication names,
  dose times) are visible to the configured messaging provider and chat
  members, and are not end-to-end encrypted. It recommends a private/DM
  channel.
