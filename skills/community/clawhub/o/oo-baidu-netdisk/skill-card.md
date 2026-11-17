## Description:

Use this skill for Baidu Netdisk requests to read, search, create, update, and delete data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected OOMOL account use this skill to inspect Baidu Netdisk account and quota details, find and download files, and manage files, folders, text files, and share links. It guides the agent to inspect each action's schema and confirm state-changing actions before running them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute remote code whose source and effects have not been verified.

Mitigation: Review the installer's source, version, and effects on installed agent skills before approving installation.

Risk: Downloading files copies them to connector transit storage, and transfer approval and access or deletion details are unclear.

Mitigation: Before downloading sensitive files, explicitly authorize the connector-storage copy and establish who can access it and when it will be deleted.

Risk: Write and move actions can change Baidu Netdisk data.

Mitigation: Confirm the exact payload and effect before writes; explicitly approve the target before destructive moves.

## Reference(s):

- [Baidu Netdisk](https://pan.baidu.com)
- [Baidu Netdisk API documentation](https://pan.baidu.com/union/doc/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, JSON]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific inputs are checked against the live connector schema; state-changing actions require user confirmation.]

## Skill Version(s):

1.0.7 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
