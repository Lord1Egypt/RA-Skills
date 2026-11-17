## Description:

Search Taobao and 1688 products, and fetch product details, through the Onebound platform gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeff2011eng](https://clawhub.ai/user/jeff2011eng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search Taobao, Tmall, and 1688 product listings and fetch item detail data through a Onebound platform API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing the gateway configuration can send ONEBOUND_API_KEY to an unintended server.

Mitigation: Use the default gateway unless another HTTPS gateway is intentionally trusted, and rotate ONEBOUND_API_KEY if it may have been sent to an unexpected host.

Risk: Shared environment files or agent launchers can alter the gateway setting before the skill runs.

Mitigation: Review environment configuration before installing or running the skill, especially in shared agent environments.

## Reference(s):

- [Onebound Platform Gateway Reference](artifact/references/api-docs.md)
- [Onebound Platform Gateway](https://onebound.vercel.app)
- [ClawHub Skill Page](https://clawhub.ai/jeff2011eng/skills/onebound-api)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown containing formatted JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ONEBOUND_API_KEY; uses curl and jq; do not expose the API key in output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
