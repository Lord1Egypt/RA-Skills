## Description:

Linear Todos is a source-execution CLI skill that helps agents create, list, complete, snooze, and review Linear todos with natural-language dates, priorities, and scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avegancafe](https://clawhub.ai/user/avegancafe)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Linear-backed todos from an agent or CLI, including creating reminders, scheduling due dates, reviewing current work, and marking items complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance can lead users toward curl-piped shell installation for uv.

Mitigation: Prefer an already installed uv or a package-manager installation before running the skill.

Risk: The setup command can save a Linear API key in plaintext configuration under ~/.config/linear-todos/config.json.

Mitigation: Use a dedicated minimal Linear API key and prefer the LINEAR_API_KEY environment variable to avoid persisted credentials.

Risk: Timezone fallback can read OpenClaw USER.md when LINEAR_TIMEZONE is not explicitly configured.

Mitigation: Set LINEAR_TIMEZONE explicitly when profile-file fallback is not desired.

Risk: Example cron entries could create recurring executions if a user manually installs them.

Mitigation: Add cron entries only after reviewing the examples and intentionally choosing scheduled runs.

## Reference(s):

- [ClawHub Linear Todos listing](https://clawhub.ai/avegancafe/skills/linear-todos)
- [Linear API settings](https://linear.app/settings/api)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration]

**Output Format:** [CLI text and optional JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates Linear issues through HTTPS API calls when commands are executed.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
