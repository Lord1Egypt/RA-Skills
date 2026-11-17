## Description:

Interface and link health assessment with error counter analysis, optical power monitoring, discard diagnosis, and utilization trending for Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers and operations teams use this skill to assess interface and link health, investigate packet loss or degraded throughput, and produce severity-ranked findings for errors, discards, optical readings, resets, flaps, and utilization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security evidence says the read-only label is contradicted by commands and recommendations that can change or disrupt network devices.

Mitigation: Use the skill for observation and reporting only unless a human approves the exact command, device, interface, timing, and rollback plan.

Risk: Counter-clearing, shutdown/no shutdown, and other remediation advice can remove diagnostic state or interrupt production links if executed without review.

Mitigation: Require explicit human approval before allowing an agent to execute counter-clearing, interface recovery, or remediation steps.

## Reference(s):

- [Interface Health CLI Reference](artifact/references/cli-reference.md)
- [Interface Health Threshold Tables](artifact/references/threshold-tables.md)
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/interface-health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline CLI command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-ranked findings, threshold comparisons, diagnostic interpretation, and remediation recommendations for human review.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
