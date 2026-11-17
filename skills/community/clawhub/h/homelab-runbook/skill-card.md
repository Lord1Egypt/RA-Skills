## Description:

Scan and document running services on this machine, including Docker containers, system services on macOS or Linux, and open listening ports, then generate a human-readable Markdown runbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, homelab operators, and system administrators use this skill to inventory active services on a host and produce a Markdown runbook for documentation, review, or scheduled snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated runbooks can expose sensitive host inventory details such as services, ports, container names, images, mount names, and process details.

Mitigation: Keep generated reports out of public repositories and shared folders, and share them only with people who should see the host inventory.

Risk: Running port scans with elevated privileges may reveal broader host details than an ordinary user-level scan.

Mitigation: Use sudo only when intentionally seeking broader port visibility.

## Reference(s):

- [Customization Guide](references/customization.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/homelab-runbook)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown runbook with summarized agent guidance and optional JSON scanner inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated runbook to a user-specified file path; scanner scripts emit JSON to stdout.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
