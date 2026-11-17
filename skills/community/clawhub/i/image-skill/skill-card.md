## Description:

Generates and edits images through Luxin's hosted service, with named model choices and recoverable results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgwilson](https://clawhub.ai/user/danielgwilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or edit images from prompts, then retrieve generated media and cost receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to send task commands and diagnostics to hosted feedback without first obtaining permission.

Mitigation: Make hosted feedback opt-in and review and redact its contents before submission.

Risk: Generated media URLs have no signature or expiry, so hosted results may remain accessible through durable links.

Mitigation: Avoid confidential material unless durable hosted result links are acceptable.

Risk: The external CLI and backend were not audited.

Mitigation: Prefer reviewed, pinned package versions and workspace-scoped installation, and set a spending limit.

## Reference(s):

- [Luxin homepage](https://luxin.sh)
- [Luxin agent guidance](https://luxin.sh/llms.txt)
- [Luxin skill contract](https://luxin.sh/skill.md)
- [Luxin full skill guidance](https://luxin.sh/skill-core.md)
- [Luxin CLI reference](https://luxin.sh/cli.md)
- [Luxin hosted API](https://api.luxin.sh)
- [ClawHub skill listing](https://clawhub.ai/danielgwilson/skills/image-skill)
- [Publisher profile](https://clawhub.ai/user/danielgwilson)

## Skill Output:

**Output Type(s):** [Images, Text, JSON]

**Output Format:** [Generated image media with hosted URLs and JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include recoverable job IDs and cost receipts.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
