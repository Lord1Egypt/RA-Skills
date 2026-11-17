## Description:

Openclaw Visual Configuration Assistant. Provides secure wizard for local/Git backup and workspace migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donnieclaw](https://clawhub.ai/user/donnieclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to open a local browser assistant that prepares backup, restore, migration, and environment setup commands for manual review and execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shell commands may modify profile files, restore files, or otherwise change the local environment if copied into a terminal.

Mitigation: Inspect every generated command before running it, with extra care for commands that write to ~/.bash_profile, install packages, restore files, or change Git state.

Risk: Git mode uses a GitHub Personal Access Token, and evidence notes verified flaws that could expose a token.

Mitigation: Use a fine-grained token limited to one trusted private backup repository, avoid broad classic repo tokens, and close the browser tab or clear stored data after use.

Risk: Backup and restore workflows can propagate unsafe or untrusted OpenClaw configuration files.

Mitigation: Use only trusted openclaw.json files and repositories, and review restored configuration before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donnieclaw/skills/octool)
- [Publisher profile](https://clawhub.ai/user/donnieclaw)
- [Project homepage listed in skill metadata](https://github.com/donnieclaw/octool)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [HTML interface with displayed plaintext shell command snippets and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands require manual review and execution; the browser tool does not auto-execute shell commands.]

## Skill Version(s):

1.0.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
