## Description:

Safely update OpenClaw with pre-flight checks and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigsan](https://clawhub.ai/user/bigsan)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to update OpenClaw, run pre-flight checks, preserve workspace and configuration state, verify the gateway after an update, and recover by rolling back to a previous version when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance scripts make broad local changes to OpenClaw workspaces, configuration, the gateway, and the globally installed package.

Mitigation: Review the scripts before use, run the dry-run path first, and confirm workspace snapshots and configuration backups before updating or rolling back.

Risk: Rollback state and configuration backups are stored under /tmp, which can be unsafe if the state is stale or untrusted.

Mitigation: Inspect rollback state before use and prefer moving update state to a private, user-owned directory.

Risk: Telegram notification settings are sourced as shell code and include bot credentials.

Mitigation: Keep the Telegram environment file private, do not source untrusted files, and use a narrowly scoped bot token.

Risk: Rollback installs a version with npm install -g based on recorded state.

Mitigation: Validate the recorded OpenClaw version before rollback and confirm global package changes are acceptable for the host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigsan/skills/openclaw-updater)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for pre-update checks, Telegram notification setup, post-update verification, and rollback.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
