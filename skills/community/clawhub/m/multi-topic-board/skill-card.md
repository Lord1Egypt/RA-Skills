## Description:

Multi-Topic Board tracks unresolved agent discussions, updates aging days, sends timeout alerts after 3 days without a task, and helps generate execution tasks in tasks/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kzclaw](https://clawhub.ai/user/kzclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve unresolved discussion topics across sessions, surface pending decisions, and convert stale topics into follow-up task files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may establish persistent workspace-level topic memory and recurring background checks.

Mitigation: Install only when ongoing topic tracking is intended, and confirm the exact cron jobs, files, session access, retention period, sensitive-topic exclusions, and removal steps before use.

Risk: Tracked discussion topics may include confidential or sensitive information.

Mitigation: Avoid using the skill for confidential discussions unless retention, access controls, and sensitive-topic exclusions are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kzclaw/skills/multi-topic-board)
- [ClawHub publisher profile](https://clawhub.ai/user/kzclaw)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace files including memory/multi-topic.md, HEARTBEAT.md, and tasks/*.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
