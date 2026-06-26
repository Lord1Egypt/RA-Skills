## Description: <br>
MoneySharks is an autonomous Aster DEX perpetual futures trading agent that can onboard credentials, run paper or live trading cycles, manage orders and positions, enforce configured risk limits, journal decisions, and review trade outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharksdotmoney](https://clawhub.ai/user/sharksdotmoney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and operate an Aster DEX futures trading agent for paper testing, approval-gated proposals, or autonomous live execution after explicit onboarding consent. It is intended for users who understand the risks of real-money leveraged futures trading and want automated scanning, sizing, execution, monitoring, journaling, and emergency controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform autonomous real-money leveraged futures trading after onboarding consent. <br>
Mitigation: Start in paper mode, review the generated configuration, and enable autonomous_live only after explicit consent and risk-cap review. <br>
Risk: Exchange API credentials grant private account access and may allow trading actions. <br>
Mitigation: Use the narrowest possible API permissions, keep ASTER_API_KEY and ASTER_API_SECRET in environment variables, and avoid storing secrets in config files. <br>
Risk: A custom ASTER_BASE_URL could redirect requests to an untrusted endpoint. <br>
Mitigation: Do not override ASTER_BASE_URL unless the endpoint is fully trusted. <br>
Risk: Autonomous execution can continue on a schedule if cron jobs are enabled. <br>
Mitigation: Review cron registration before enabling it and use the documented halt, circuit breaker, cancel-order, flatten-position, and paper-mode controls when needed. <br>


## Reference(s): <br>
- [MoneySharks ClawHub listing](https://clawhub.ai/sharksdotmoney/moneysharks) <br>
- [MoneySharks documentation](documentation-moneysharks.md) <br>
- [Live execution boundary](references/live-execution-boundary.md) <br>
- [Risk policy](references/risk-policy.md) <br>
- [Emergency controls](references/emergency-controls.md) <br>
- [Onboarding and consent](references/onboarding.md) <br>
- [Aster read-only integration](references/aster-readonly-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON status/configuration files, and shell commands for local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASTER_API_KEY and ASTER_API_SECRET for private Aster actions; default mode is paper until onboarding consent enables live autonomy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
