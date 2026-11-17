## Description:

Trade Ostium RWA perpetuals on Arbitrum through CAI using market lookup, preflight checks, trade placement, order status polling, and hosted enrollment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through CAI-managed Ostium perpetual trading on Arbitrum, including setup, enrollment, preflight validation, order placement, status checks, and position closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides an agent through high-risk leveraged Ostium perpetual trading through CAI.

Mitigation: Install it only for intended CAI/Ostium trading workflows and require explicit confirmation before opening, closing, or increasing leveraged positions.

Risk: Broad CAI API scope and funded custodial balances can increase financial exposure.

Mitigation: Use the narrowest available CAI API scope and keep funded balances limited to amounts the user is willing to risk.

Risk: Incorrect market, preflight, or order-status handling could lead to unintended trading actions.

Mitigation: Resolve pair IDs from live markets, run preflight checks until valid, and poll order status until terminal before taking follow-up action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/ostium-with-cai)
- [CAI skill reference](https://cai.com/skill.md)
- [CAI tools manifest](https://cai.com/specs/cai-tools.manifest.json)
- [CAI developer documentation](https://cai.com/developers.html)
- [Publisher profile](https://clawhub.ai/user/bernardtai)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with API tool names and shell command setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CAI_API_KEY with platform or full API scope; intended flows include hosted enrollment, preflight checks, explicit trade actions, and order status polling.]

## Skill Version(s):

1.0.18 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
