## Description:

Guides an agent through a checked OpenClaw upgrade workflow with backup, gateway restart monitoring, and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliahmadaziz](https://clawhub.ai/user/aliahmadaziz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when they need an agent to check and run an OpenClaw upgrade, preserve local configuration and cron state, restart the gateway, and recover from failed upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upgrade workflow can run workspace hook scripts during the upgrade process.

Mitigation: Review or remove optional workspace hook scripts before use, and run only in workspaces where local scripts are trusted.

Risk: The workflow can add, commit, and push the whole workspace after an upgrade.

Mitigation: Run from a clean workspace, inspect the configured git remote first, and disable or require explicit confirmation for automatic git operations.

Risk: Using an unpinned latest OpenClaw version can apply an unexpected release.

Mitigation: Prefer a pinned and verified OpenClaw version and confirm the intended upgrade target before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aliahmadaziz/skills/openclaw-safe-upgrade)
- [ClawHub publisher profile](https://clawhub.ai/user/aliahmadaziz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and status-check instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for read-only checks, upgrades, forced upgrades, rollback, and post-restart result review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
