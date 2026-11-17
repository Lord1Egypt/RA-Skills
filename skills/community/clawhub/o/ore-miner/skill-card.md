## Description:

Autonomous ORE mining on Solana via refinORE, including onboarding, session start/stop, tile strategy optimization, P&L tracking, risk management, auto-restart, multi-coin mining, DCA and limit orders, and staking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jusscubs](https://clawhub.ai/user/jusscubs)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to help an agent configure refinORE access, check wallet and session state, start and stop ORE mining sessions, adjust tile strategies, and track mining P&L. It is intended for users who knowingly want agent-assisted crypto-mining and automated refinORE activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a persistent API key to start recurring crypto-mining and automated trading actions.

Mitigation: Install only when agent-managed refinORE activity is intended; use a narrowly scoped, revocable API key and require explicit confirmation before mining, auto-restart, DCA, limit order, edit, or delete actions.

Risk: Automated mining or trading can spend funds or continue activity beyond the user's intended risk tolerance.

Mitigation: Set independent spending and loss limits outside the skill and require confirmation before changing deployment amounts or risk settings.

Risk: Credential or endpoint misuse could expose the refinORE API key or direct requests to an unintended service.

Mitigation: Pin REFINORE_API_URL to the legitimate refinORE endpoint and avoid passing the API key as a command-line argument.

## Reference(s):

- [ORE Miner on ClawHub](https://clawhub.ai/jusscubs/skills/ore-miner)
- [refinORE application](https://automine.refinore.com)
- [refinORE API Endpoints](references/api-endpoints.md)
- [ORE V2 Mining Rules & Mechanics](references/mining-rules.md)
- [ORE Mining Strategies](references/strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REFINORE_API_URL and REFINORE_API_KEY; bundled helper scripts expect bash, curl, and python3.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
