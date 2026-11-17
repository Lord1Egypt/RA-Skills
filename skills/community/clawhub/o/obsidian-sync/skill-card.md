## Description:

Sync files between Clawdbot workspace and Obsidian. Run the sync server to enable two-way file synchronization with the OpenClaw Obsidian plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andybold](https://clawhub.ai/user/andybold)

### License/Terms of Use:


## Use Case:

Developers and Obsidian users use this skill to run a local sync server that lets OpenClaw synchronize markdown notes between an Obsidian vault and a Clawdbot workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync server has a file-containment flaw and can read or write workspace files reachable through configured sync paths.

Mitigation: Use only trusted clients, keep backups of notes, avoid syncing directories containing symlinks, and run the service under a dedicated low-privilege account.

Risk: Changing the bind address or exposing the service can make the sync API reachable beyond the local machine.

Mitigation: Keep the bind address on localhost unless the exposure is intentional, and protect access with a strong token.

Risk: The optional systemd linger service can keep the sync server running after logout and at boot.

Mitigation: Enable linger only when persistent background operation is required and has been reviewed.

## Reference(s):

- [Obsidian OpenClaw plugin](https://github.com/AndyBold/obsidian-openclaw)
- [BRAT plugin installer](https://github.com/TfTHacker/obsidian42-brat)
- [ClawHub skill page](https://clawhub.ai/andybold/skills/obsidian-sync)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON HTTP responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a Node.js HTTP sync server that lists, reads, writes, and reports status for markdown files under configured workspace paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
