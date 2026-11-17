## Description:

Guides agents through SQL-based Hologres AI Function workflows to generate ad images and videos, simulate virtual campaign delivery, analyze ROI, and produce strategy recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, growth analysts, and developers use this skill to prepare Hologres SQL workflows for ad asset generation, virtual delivery simulation, real-time ROI analysis, and budget recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow needs cloud storage and database authority for Hologres and OSS resources.

Mitigation: Run it only in an isolated environment with least-privileged Hologres and OSS/RAM roles.

Risk: Writable SQL templates can modify important campaign or asset data if used without review.

Mitigation: Review or rewrite templates to use parameter binding or strict validation before running them against important data.

Risk: Signed OSS URLs can act as private bearer links.

Mitigation: Treat generated signed URLs as private and avoid sharing them outside intended recipients.

Risk: Tool installation can introduce unreviewed client behavior.

Mitigation: Use a pinned, reviewed hologres-cli version before executing generated commands.

## Reference(s):

- [SQL Templates](references/sql-templates.md)
- [Style Templates](references/style-templates.md)
- [Virtual Delivery and ROI Analysis](references/virtual-delivery.md)
- [ClawHub Skill Page](https://clawhub.ai/wenbingyu/skills/hologres-ad-campaign)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for review before execution against Hologres, OSS, and campaign simulation data.]

## Skill Version(s):

0.2.0 (source: server release evidence and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
