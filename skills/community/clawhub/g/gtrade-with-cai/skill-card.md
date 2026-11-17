## Description:

Trade gTrade perps via CAI using defi_markets, defi_preflight, defi_trade, defi_order_status, and hosted /act enrollment; requires platform or full API scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare, place, monitor, and close gTrade perpetual positions through CAI after platform enablement and hosted enrollment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or close leveraged gTrade perpetual positions using live custodial funds.

Mitigation: Require explicit user confirmation for each order or close action and verify preflight and order details before calling defi_trade.

Risk: Broad CAI API scopes increase the impact of misuse or credential exposure.

Mitigation: Use the narrowest CAI API scope available, store CAI_API_KEY in secrets, and revoke or disable platform automation when it is no longer needed.

Risk: Enrollment or readiness gaps can block live trading or create incorrect assumptions about automation status.

Mitigation: Check platform_readiness and require the user to complete hosted /act enrollment before trading; do not confirm enrollment on the user's behalf.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/gtrade-with-cai)
- [CAI canonical skill reference](https://cai.com/skill.md)
- [CAI tools manifest](https://cai.com/specs/cai-tools.manifest.json)
- [CAI developers](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with inline JSON and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.17 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
