## Description:

AI-powered atomic habit tracker with natural language logging, streak tracking, smart reminders, and coaching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tralves](https://clawhub.ai/user/tralves)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Habit Flow to create and manage habits, log completions in natural language, review progress, configure reminders, and receive habit-coaching guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder and coaching features can create persistent scheduled agent jobs, and the security evidence flags unsafe shell command strings with user-controlled reminder content.

Mitigation: Review and audit created cron jobs before use, keep proactive coaching opt-in, and remove jobs that are not expected.

Risk: Untrusted habit names, reminder messages, recipients, channels, or timezone values may affect reminder command construction.

Mitigation: Use trusted values only until command construction is fixed with argument-array execution and strict validation.

Risk: Dependencies are not pinned by a lockfile in the release artifact.

Mitigation: Pin dependencies with a lockfile before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tralves/skills/habit-flow-skill)
- [Project Homepage](https://github.com/tralves/habit-flow-skill)
- [README](README.md)
- [Installation Guide](INSTALL.md)
- [Commands Reference](references/COMMANDS.md)
- [Data Storage Reference](references/DATA.md)
- [Data Schema](references/data-schema.md)
- [Reminder Technical Reference](references/REMINDERS.md)
- [Atomic Habits Coaching Reference](references/atomic-habits-coaching.md)
- [Persona Reference](references/personas.md)
- [Proactive Coaching Reference](references/proactive-coaching.md)
- [Proactive Coaching Setup Guide](docs/PROACTIVE_COACHING_SETUP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands, JSON script output, and optional generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, npm, and a clawdbot environment for reminder delivery.]

## Skill Version(s):

1.5.4 (source: SKILL.md frontmatter metadata, CHANGELOG, package.json, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
