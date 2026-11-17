## Description:

Guides agents through authorized Instagram account operations in Meta Business Suite, including inbound DM and comment replies, quota controls, recaps, and human escalation conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and business users use this skill to run authorized Instagram inbox and comment workflows through Meta Business Suite while staying within stated quotas and escalation rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Instagram DMs, comments, handles, and lead details that may include sensitive or identifiable information.

Mitigation: Use it only on accounts you own or are authorized to operate, keep local memory files access-controlled, and enforce the stated 90-day retention.

Risk: Optional webhook alerts can send recap details, including handles or lead context, outside the local workspace.

Mitigation: Leave the webhook empty by default; enable it only for trusted, access-controlled destinations after redacting sensitive details.

Risk: Automated Instagram activity can trigger platform blocks, challenges, or account review if used outside the stated limits.

Mitigation: Follow the phase gates, quotas, and stop conditions, and hand control to a human for login prompts, challenges, action blocks, or suspension events.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexbloch-ia/skills/instagram-account-operations)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes quota tables, stop conditions, local memory file conventions, and recap templates.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
