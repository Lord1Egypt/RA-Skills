## Description:

Diagnoses common Linux service issues using logs, systemd/PM2, file permissions, Nginx reverse proxy checks, and DNS sanity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose failing Linux services, PM2 processes, Nginx reverse proxy issues, DNS problems, and file permission errors, then plan minimal fixes and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative repair commands can change service state, Nginx configuration, or file ownership and permissions.

Mitigation: Keep diagnosis read-only by default, require explicit approval before changes, test Nginx configuration before reload, and include verification and rollback steps.

Risk: Incomplete logs, status output, or service details can lead to an incorrect root-cause assessment.

Mitigation: Ask for missing logs or status output before concluding, and ground the triage report in evidence supplied by the user.

## Reference(s):

- [Linux Service Triage Commands](references/triage-commands.md)
- [ClawHub skill page](https://clawhub.ai/kowl64/skills/linux-service-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown triage report with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exact fix commands are provided only when explicitly requested and safe.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
