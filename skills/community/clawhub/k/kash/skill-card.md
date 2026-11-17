## Description:

Pay for APIs, tools, and services from your agent's Kash wallet. Spends below $5 are autonomous; above $5 requires explicit user YES. Requires KASH_KEY and KASH_AGENT_ID from kash.dev.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devfaraaz](https://clawhub.ai/user/devfaraaz)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to let an OpenClaw agent pay for external APIs, tools, and services from a Kash wallet before paid operations. It is intended for payment-gated workflows where local confirmation thresholds and server-side wallet controls govern agent spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Misconfiguration could expose the Kash API key or route spend traffic incorrectly.

Mitigation: Review before installing, use a low-privilege Kash agent key, and keep KASH_API_URL unset unless doing local development.

Risk: Local budget and confirmation controls may not be sufficient on their own.

Mitigation: Set server-side budgets in the Kash dashboard and treat the server-side controls as authoritative.

Risk: Incorrect budget or confirmation values could allow unintended autonomous spend.

Mitigation: Set numeric KASH_BUDGET and KASH_SPEND_CONFIRMATION_THRESHOLD values carefully, and lower the confirmation threshold when every spend should require explicit approval.

## Reference(s):

- [Kash homepage](https://kash.dev)
- [ClawHub skill page](https://clawhub.ai/devfaraaz/skills/kash)
- [Publisher profile](https://clawhub.ai/user/devfaraaz)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Plain text status messages and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs include spend approval, budget, authorization, pause, and API error statuses.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
