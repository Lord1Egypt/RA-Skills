## Description:

Automates rotating backups and restores of OpenClaw workspaces, configuration, strategies, and skills to WebDAV storage, with GPG-supported credential storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[king6381](https://clawhub.ai/user/king6381)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to configure WebDAV backups, run rotating workspace backups, and restore OpenClaw state after data loss or machine replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore operations can overwrite OpenClaw memory, configuration, strategies, and installed skills.

Mitigation: Keep a separate local backup and inspect or verify downloaded archives before using automatic restore modes.

Risk: The remote WebDAV server may be able to read backup contents if payload encryption is not fixed.

Mitigation: Use only trusted HTTPS WebDAV endpoints and treat server-side storage as sensitive.

Risk: Standalone restore bootstrap behavior can install system software from network sources.

Mitigation: Review the restore kit before running it, especially on machines that already contain trusted OpenClaw state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/king6381/skills/mjolnir-shadow)
- [Project homepage](https://github.com/king6381/mjolnir-shadow)
- [Configuration reference](references/config-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration files and compressed backup archives and transfer them to WebDAV when scripts are executed.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
