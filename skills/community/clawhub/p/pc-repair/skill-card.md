## Description:

电脑维修智能助手通过交互式问诊诊断常见电脑故障，比较自救、DIY 和专业维修方案，并生成维修建议、成本估算、配件建议和可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to triage desktop or laptop faults, compare repair options, estimate costs, check upgrade compatibility, and decide when professional repair is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair guidance may include disk, partition, driver, system repair, or reboot operations that can change system state or cause data loss.

Mitigation: Back up important data first, explain the expected impact, and ask for explicit confirmation before admin-level, rebooting, disk, partition, or recovery commands.

Risk: Recommended third-party utilities may be downloaded from unsafe or spoofed sources.

Mitigation: Use official vendor sources, verify checksums or signatures when available, and avoid broadly trusting tools flagged by antivirus.

Risk: Hardware handling can damage components, void warranties, or create electrical and static-discharge hazards.

Mitigation: Power down and unplug devices, use static precautions, check warranty status, and recommend professional repair for uncertain or high-risk procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/pc-repair)
- [Common fault diagnostic flows](references/common_faults.md)
- [Parts compatibility checklist](references/parts_compatibility.md)
- [Repair cost reference](references/repair_costs.md)
- [Repair tool guide](references/tool_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown repair guidance with tables, command snippets, and optional HTML report code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic questions, cost estimates, compatibility checklists, purchasing guidance, tool recommendations, and safety warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
