## Description:

Turn seller-supplied nutrition facts into one nutrition panel still per SKU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and agents use this skill to turn seller-confirmed nutrition tables and named SKUs into SKU-ordered nutrition panel stills for food packaging or product listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a shared, persistent Beatra account token with authority beyond nutrition-panel image generation.

Mitigation: Use the skill only with a trusted Beatra account, keep the token private, and reconnect or switch accounts only through the documented authorization flow.

Risk: Automatic updates are enabled by default and may replace installed package code.

Mitigation: Disable automatic updates with the documented `python3 scripts/mcp_client.py update --auto off` command when reviewed code must remain pinned.

Risk: Reference uploads may contain sensitive product or brand materials.

Mitigation: Avoid uploading sensitive reference files unless the user accepts the Beatra upload path and destination constraints.

Risk: Generated nutrition-panel small type may be incorrect or unreadable.

Mitigation: Review visible printed lines against seller-confirmed facts and do not treat the generated still as a certified legal nutrition label.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/nutrition-panel-art)
- [Beatra Skill Homepage](https://beatra.ai/skills/nutrition-panel-art)
- [Nutrition-panel workflow](references/workflow.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Installation and authentication](references/installation-and-auth.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated image files or artifact IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one nutrition panel still per SKU, plus task IDs, resolved models, dimensions, formats, and net charged credits when available.]

## Skill Version(s):

0.1.3 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
