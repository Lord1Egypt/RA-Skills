## Description:

Trade Hyperliquid perpetuals through CAI using CAI DeFi tools for market discovery, preflight checks, order placement, and order status tracking without separate Hyperliquid website signup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide CAI-enabled Hyperliquid perpetual trading workflows, including readiness checks, enrollment, market lookup, preflight validation, order placement, status polling, closing, and cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Hyperliquid perpetual trading can create real financial losses, including leveraged trading losses.

Mitigation: Confirm asset, side, size, price, and order intent before any live trade, and use preflight validation before placement.

Risk: Deposits and approveAgent authorization can enable live trading through the CAI custodial workflow.

Mitigation: Use platform API scope instead of full scope when possible and authorize only when the user intends to trade Hyperliquid perpetuals.

Risk: The artifact states the Hyperliquid automation path is partial_live until enrollment and trade smoke tests pass.

Mitigation: Treat enrollment, deposit readiness, and first trades as review points; verify status with defi_order_status until terminal before taking follow-up actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bernardtai/skills/hyperliquid-with-cai)
- [CAI Canonical Skill Reference](https://cai.com/skill.md)
- [CAI Tools Manifest](https://cai.com/specs/cai-tools.manifest.json)
- [CAI Developers](https://cai.com/developers.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown guidance with inline shell commands and CAI tool parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAI_API_KEY and platform or full API scope; live trades require user confirmation.]

## Skill Version(s):

1.0.17 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
