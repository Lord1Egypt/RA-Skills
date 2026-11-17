## Description:

Raspberry Pi system administration. Monitor resources, manage services, perform updates and maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers, operators, and Raspberry Pi administrators use this skill to inspect Pi host status, troubleshoot network and service issues, and run maintenance tasks such as package updates, cleanup, reboot, gateway restart, and system optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reboot the host, kill and restart services, and persistently change system settings.

Mitigation: Install only on a Raspberry Pi you administer and require human review before invoking maintenance commands.

Risk: The security guidance identifies misleading or under-scoped controls, including confirmation behavior, dry-run side effects, hardcoded gateway paths and addresses, port mismatch, and optimization undo logic.

Mitigation: Review and fix these behaviors before allowing agents or automation to invoke maintenance commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thesethrose/skills/pi-admin)
- [Source Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may inspect host state or perform privileged maintenance actions when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
