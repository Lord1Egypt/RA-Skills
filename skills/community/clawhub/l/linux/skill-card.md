## Description:

Debugs and hardens Linux hosts across permissions, storage, memory, processes, systemd, scheduling, networking, SSH, boot, package, desktop, and security issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and system administrators use this skill to diagnose Linux host failures, propose safer operational commands, harden exposed systems, and record durable host state or incident notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can accumulate sensitive operational inventory, host, contact, incident, baseline, change, and access-reference notes under local Clawic data paths.

Mitigation: Review before installing, use restrictive filesystem permissions on the Clawic data directories, and disable or override memory writes for one-off troubleshooting when persistent notes are not desired.

Risk: Troubleshooting sessions may include secrets or credentials in pasted logs, unit files, environment files, shell history, or configuration snippets.

Mitigation: Avoid pasting secrets; when persistent notes are needed, store only pointers such as file, environment variable, keychain, or vault references rather than credential values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/linux)
- [Clawic Linux skill page](https://clawic.com/skills/linux)
- [Clawic skill library](https://clawic.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, checklists, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local note updates under configured Clawic data paths when troubleshooting produces durable host, incident, baseline, change, or runbook information.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
