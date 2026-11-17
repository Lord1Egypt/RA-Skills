## Description:

PC Health Check helps an agent run Windows health diagnostics for CPU, memory, disk, network, processes, devices, system events, startup items, listening ports, and security updates, then summarize the results with risk levels and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolfzb](https://clawhub.ai/user/coolfzb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support engineers use this skill to inspect the health of a Windows PC and receive a structured diagnostic report with issue severity and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can contain host-specific system, process, startup, event log, listening port, and update details.

Mitigation: Review and redact reports before sharing them outside the trusted support or operations context.

Risk: Some diagnostic checks may require broader Windows access to retrieve driver, event, update, or network details.

Mitigation: Run the skill only in trusted local environments and review requested access before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolfzb/skills/pc-health-check)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown health reports and JSON diagnostic results, with optional shell commands for running the local Node.js script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include host-specific system, process, startup, event log, listening port, and update details.]

## Skill Version(s):

1.0.1 (source: artifact/SKILL.md frontmatter and artifact/CHANGELOG.md; release metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
