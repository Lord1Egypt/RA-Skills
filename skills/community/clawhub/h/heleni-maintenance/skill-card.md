## Description:

Unified workspace maintenance skill for backing up a workspace to GitHub, updating OpenClaw and installed skills, and cleaning stale session-store entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run workspace maintenance tasks, including GitHub backups, OpenClaw and skill updates, and session-store cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create recurring cron jobs and silently push the entire workspace to GitHub.

Mitigation: Require explicit approval for each backup action, disclose scheduled jobs, and disable silent backup behavior unless it is intentionally configured by the owner.

Risk: The skill can inspect raw GitHub tokens and credentials.

Mitigation: Do not print tokens, prefer scoped credential helpers or environment validation, and scan staged files for secrets before any push.

Risk: The skill can update OpenClaw and all installed skills from broad update sources.

Mitigation: Pin update sources or versions where possible, review release notes before updating, and verify service health after changes.

Risk: The skill can directly edit session-store state.

Mitigation: Run session cleanup as a separately approved maintenance task, back up the session store first, and limit cleanup to stale cron-run entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/heleni-maintenance)
- [Publisher profile](https://clawhub.ai/user/netanel-abergel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status-report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose scheduled cron jobs, Git operations, platform updates, and session-store cleanup actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
