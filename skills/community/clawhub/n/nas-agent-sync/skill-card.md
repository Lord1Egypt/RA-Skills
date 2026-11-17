## Description:

Synology NAS integration for OpenClaw centralized file storage for multi-agent teams via SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neal-collab](https://clawhub.ai/user/neal-collab)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to centralize multi-agent file storage on a Synology NAS or other SSH-accessible storage host. It provides setup guidance for a File Master agent, shared folder structure, file retrieval, and backup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad SSH-backed file access can expose or alter more NAS data than intended.

Mitigation: Use a dedicated low-privilege NAS account and restrict each agent to approved directories.

Risk: Unvalidated file paths or shell-sensitive input can lead to unauthorized access or command injection.

Mitigation: Validate and canonicalize requested paths, and reject absolute paths, '..', control characters, and shell metacharacters.

Risk: Scheduled memory backups can retain sensitive data without review.

Mitigation: Review backup scope, encrypt backups at rest, enforce access controls, and define retention limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neal-collab/skills/nas-agent-sync)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, JSON, and AGENTS.md snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes NAS setup, File Master routing, troubleshooting, and backup guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
