## Description:

MagicHaqi Operator is an owner-only agent skill for running MagicHaqi operations across companionship care, content production, marketing material generation, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paraengine](https://clawhub.ai/user/paraengine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or owners of a MagicHaqi workspace use this skill to run a recurring operational loop that maintains a demo pet, produces owner-reviewed content and marketing assets, and summarizes local operational KPIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests long-running authority to mutate local MagicHaqi state and generated content.

Mitigation: Use only in an owner-controlled MagicHaqi workspace and route local content or state writes through review or staging before publishing or committing generated files.

Risk: The skill uses URL token login patterns that can expose credentials if real tokens are embedded in links or logs.

Mitigation: Avoid putting real tokens in URLs and review logs or shared artifacts for token leakage.

Risk: Analytics may include sdk.remoteLog telemetry if it is available in the workspace.

Mitigation: Clarify or disable sdk.remoteLog unless remote telemetry is intentionally part of the analytics workflow.

Risk: Content and marketing tasks could create spammy output or use unauthorized external intellectual property.

Mitigation: Keep the documented production throttles, require owner approval before third-party publishing, and keep external IP only when it is explicitly marked authorized.

## Reference(s):

- [MagicHaqi Operator on ClawHub](https://clawhub.ai/paraengine/skills/haqi-operator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline commands, local file updates, generated content drafts, and KPI summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces material for owner review and local MagicHaqi workspace state; it is not intended to auto-publish to third-party services.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
