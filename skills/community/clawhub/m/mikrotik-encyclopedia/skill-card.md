## Description:

MikroTik RouterOS documentation-first workflow for MikroTik-specific questions, troubleshooting, command planning, live CLI/API work, config review, log analysis, security review, performance tuning, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and operators use this skill to answer MikroTik RouterOS questions, plan commands, review configurations, troubleshoot logs, and prepare safer live CLI/API work against MikroTik devices. It emphasizes official MikroTik documentation, local cache checks, and clear separation between documented behavior, observed device state, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local notes and inventory can expose sensitive network details if shared or backed up without review.

Mitigation: Keep .MikroTik-Encyclopedia in a private workspace, review it before sharing or backup, and do not store passwords, tokens, private URLs, management addresses, or unnecessary topology details.

Risk: Live MikroTik CLI/API work can affect routing, firewalling, VLANs, CAPsMAN, DNS/DHCP, management access, or device reachability.

Mitigation: Confirm the target and intended action, inspect current state first, and consult official MikroTik documentation before non-trivial or high-impact changes.

Risk: Cached documentation or local observations can become stale or be mistaken for official behavior.

Mitigation: Use cached material as a starting point, refresh official documentation for version-sensitive questions, and label answers as official docs, observed local state, or inference.

## Reference(s):

- [MikroTik Documentation](https://help.mikrotik.com/docs/)
- [MikroTik RouterOS Filter Documentation](https://help.mikrotik.com/docs/display/ROS/Filter)
- [MikroTik Encyclopedia Workflow](references/workflow.md)
- [MikroTik Encyclopedia Cache Layout](references/cache-layout.md)
- [MikroTik Topic Map](references/topic-map.md)
- [ClawHub Skill Page](https://clawhub.ai/kklouzal/skills/mikrotik-encyclopedia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline RouterOS, CLI, API, or shell command snippets and optional workspace-local cache or note files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update files under .MikroTik-Encyclopedia for cached official documentation, device notes, pattern notes, and inventory; notes should not contain plaintext secrets.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
