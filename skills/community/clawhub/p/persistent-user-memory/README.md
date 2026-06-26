# 🧠 persistent-user-memory

> An OpenClaw skill that makes your agent actually remember you.

---

## The Problem

Every time OpenClaw starts a new session, it forgets everything.

It doesn't know your name. It doesn't know that you hate morning meetings, that "Sarah" means Ms. Chen your most important client, or that the last deployment failed because of a missing env var. You repeat yourself constantly, and the agent never gets better at working *with you specifically*.

**That's what this skill fixes.**

---

## What It Does

`persistent-user-memory` gives OpenClaw a structured, local memory of you that grows over time:

- 👤 **Identity & preferences** — tone, schedule, tools, working hours
- 🤝 **Relationships** — who your contacts are, how to communicate with them
- 🔁 **Patterns** — recurring tasks, common mistakes, frequent requests
- 📓 **Episodic log** — a running summary of significant past interactions

The agent reads this memory before acting and updates it after learning — silently, without interrupting your workflow.

---

## Install

```bash
claw skill install persistent-user-memory
```

Or manually:

```bash
mkdir -p ~/.openclaw/skills/persistent-user-memory
cp SKILL.md ~/.openclaw/skills/persistent-user-memory/SKILL.md
```

---

## How It Works

### Before every significant action
The agent loads your profile and applies relevant context automatically.

> You ask it to email "David" → it checks your contacts, finds two Davids, asks which one rather than guessing.

### After every learning moment
When you correct the agent, state a preference, or complete a recurring task, memory is updated.

> You say "never schedule before 9:30am" → stored immediately, respected forever.

### Proactively, when it matters
The agent surfaces past context when it's genuinely useful — not constantly.

> "Last time you ran this deploy it failed due to a missing env var — want me to check first?"

---

## Privacy

- ✅ All memory stored **locally only** at `~/.openclaw/memory/user_profile.json`
- ✅ Never sent raw to any remote server or API
- ✅ Only relevant subsets passed to the LLM per task
- ✅ Full deletion on request — surgical or complete
- ❌ Never stores passwords, payment info, or raw message contents

---

## Edge Cases Handled

| Situation | Behavior |
|-----------|----------|
| Conflicting preferences | Surfaces conflict, waits for resolution before writing |
| Ambiguous contacts | Asks for clarification, never guesses |
| Sensitive data request | Refuses politely, suggests secure alternatives |
| Corrupted memory file | Backs up, starts fresh, offers recovery |
| First run (no file) | Learns passively, no onboarding questionnaire |
| "What do you know about me?" | Returns human-readable summary, not raw JSON |
| "Forget [X]" | Confirms scope, surgically removes only what's specified |

---

## Example Profile

See [`examples/user_profile.example.json`](examples/user_profile.example.json) for a fully filled-in sample.

---

## Contributing

PRs welcome. Especially interested in:
- Support for vector store backends (for semantic memory search)
- Multi-user profiles (shared machines)
- Encrypted memory file option
- Additional contact relationship types

Please open an issue before submitting large changes.

---

## Security

This skill handles personal data and filesystem access. If you find a vulnerability, please open a **private** security advisory rather than a public issue.

Given recent concerns around malicious ClawHub skills, this repo welcomes independent security audits. The full skill logic is in a single readable `SKILL.md` — no hidden scripts, no remote calls.

---

## License

MIT

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md)
