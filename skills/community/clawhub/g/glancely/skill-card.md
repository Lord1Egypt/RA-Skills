## Description:

Personal tracker framework. Scaffold new habit/workout/mood/reminder trackers from natural language. Dashboard, cron, all in one skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junjieyu95](https://clawhub.ai/user/junjieyu95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use Glancely to create and operate local personal trackers for habits, mood, reminders, diary entries, and Most Important Task workflows. The skill guides an agent to scaffold tracker components, run setup and logging commands, schedule prompts, and build a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run discovered local tracker component code under the Glancely home directory.

Mitigation: Review component SKILL.md files and scripts before allowing the agent to execute logging, stats, dashboard, or scaffold workflows.

Risk: The skill may register persistent OpenClaw cron prompts and reminders.

Mitigation: Confirm cron schedules and notification text before registration, and periodically inspect or remove entries that are no longer needed.

Risk: Diary logging can access a user's Google Calendar through locally stored OAuth credentials.

Mitigation: Use a dedicated OAuth client where practical, keep credential files local, and revoke or remove tokens when the diary feature is no longer used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/junjieyu95/skills/glancely)
- [README](artifact/README.md)
- [Component Contract](artifact/docs/component-contract.md)
- [End-to-End Test Plan](artifact/E2E_TEST_PLAN.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, generated tracker files, local configuration, and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local tracker components, SQLite-backed data, dashboard output, and optional OpenClaw cron registrations under the user's Glancely home directory.]

## Skill Version(s):

0.3.0 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
