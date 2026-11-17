## Description:

Routes industrial and operational technology data-tap and troubleshooting tasks to the appropriate iaiops edition and governed MCP profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Industrial operations engineers and automation teams use this router to choose an appropriate iaiops edition and MCP profile for OT data access and troubleshooting, including OEE, asset inventory, and data-quality work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, with medium confidence, because three local references were unresolved.

Mitigation: Review and resolve the local references before installing or relying on the skill.

Risk: Device writes can affect industrial control equipment.

Mitigation: Follow the documented read-first workflow, require the documented MOC approval for real writes, and do not write to endpoints marked SIS.

## Reference(s):

- [Industrial-AIOps release page](https://clawhub.ai/zw008/skills/iaiops)
- [Industrial-AIOps Energy repository](https://github.com/industrial-aiops/industrial-aiops-energy)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and configuration examples or drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes to an edition and profile; configuration drafts require human review.]

## Skill Version(s):

0.34.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
