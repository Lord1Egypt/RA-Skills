## Description:

Fully autonomous 24/7 Aster DEX perpetual futures trading agent that manages onboarding, live execution, bracket orders, trailing stop management, position monitoring, risk enforcement, journaling, and self-learning from past trades after explicit onboarding consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharksdotmoney](https://clawhub.ai/user/sharksdotmoney)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use MoneySharks to configure and run an Aster DEX perpetual futures trading agent. It supports paper, approval, live, and autonomous_live modes for market scanning, sizing, execution, monitoring, journaling, and trade review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended real-money futures trading can place leveraged orders and lose funds if misconfigured or insufficiently reviewed.

Mitigation: Install only when this authority is intended; start in paper mode, use restricted Aster API keys, use IP allowlisting when available, and verify risk limits before live trading.

Risk: Autonomous live mode removes per-trade approval after explicit onboarding consent.

Mitigation: Use paper or approval mode until audited, and verify approval gates, halt behavior, circuit breakers, and protective orders before enabling autonomous_live.

Risk: Aster API credentials grant trading access.

Mitigation: Store ASTER_API_KEY and ASTER_API_SECRET in environment variables, avoid hardcoding secrets, and restrict key permissions to the minimum required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sharksdotmoney/skills/moneysharks)
- [MoneySharks Documentation](artifact/documentation-moneysharks.md)
- [Onboarding](artifact/references/onboarding.md)
- [Risk Policy](artifact/references/risk-policy.md)
- [Live Execution Boundary](artifact/references/live-execution-boundary.md)
- [Execution Playbook](artifact/references/execution-playbook.md)
- [Emergency Controls](artifact/references/emergency-controls.md)
- [Aster Read-Only Integration](artifact/references/aster-readonly-integration.md)
- [Cron Automation](artifact/references/cron-automation.md)
- [Deployment](artifact/references/deployment.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON configuration and state files, and shell/Python command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate in paper, approval, live, or autonomous_live modes; live trading requires Aster API credentials and explicit onboarding consent.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
