## Description: <br>
AI-powered atomic habit tracker with natural language logging, streak tracking, smart reminders, and coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tralves](https://clawhub.ai/user/tralves) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to create and track habits, log completions in natural language, review streaks and progress, configure reminders, and receive coaching based on habit patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent scheduled reminder or coaching messages to external or last-used chat channels. <br>
Mitigation: Before enabling reminders or coaching, inspect the cron jobs and bind delivery to an explicit recipient or channel. <br>
Risk: Habit data is stored locally under ~/clawd/habit-flow-data. <br>
Mitigation: Install only when local storage of habit names, logs, reminders, and coaching configuration is acceptable. <br>
Risk: Reminder syncing has a reported shell-command injection risk when untrusted habit names or custom messages are synced. <br>
Mitigation: Avoid syncing reminders from untrusted habit names or custom messages until the shell-command construction is fixed. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/tralves/habit-flow-skill) <br>
- [Project Homepage](https://github.com/tralves/habit-flow-skill) <br>
- [Commands Reference](references/COMMANDS.md) <br>
- [Reminders Reference](references/REMINDERS.md) <br>
- [Data Storage Reference](references/DATA.md) <br>
- [Data Schema](references/data-schema.md) <br>
- [Personas Reference](references/personas.md) <br>
- [Coaching Techniques](references/atomic-habits-coaching.md) <br>
- [Proactive Coaching Reference](references/proactive-coaching.md) <br>
- [Proactive Coaching Setup](docs/PROACTIVE_COACHING_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with inline shell commands, generated JSON from helper scripts, and optional image files for habit visualizations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local habit data under ~/clawd/habit-flow-data and configure scheduled reminder or coaching jobs when enabled.] <br>

## Skill Version(s): <br>
1.5.4 (source: frontmatter, package.json, CHANGELOG, released 2026-02-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
