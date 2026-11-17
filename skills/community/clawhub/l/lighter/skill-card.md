## Description:

Interact with Lighter protocol, a ZK rollup orderbook DEX, to trade, check prices, manage positions, and query account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect Lighter markets, query account and position data, and prepare or submit Lighter trading actions from an agent workflow.

### Deployment Geography for Use:

Global, subject to Lighter's geographic restrictions.

## Known Risks and Mitigations:

Risk: The live order script can submit mainnet trades without an enforced confirmation or dry-run boundary.

Mitigation: Require an explicit confirmation or dry-run flow before using the order path, and review every order parameter before execution.

Risk: A funded or high-limit Lighter API key could authorize unintended trading activity.

Mitigation: Use isolated credentials with limited trading authority and avoid exposing funded or high-limit keys until controls are reviewed.

Risk: Dependency and order sizing behavior require review before live trading.

Mitigation: Pin and verify dependencies, then validate order sizing and price conversion before enabling order placement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aviclaw/skills/lighter)
- [Lighter API docs](https://apidocs.lighter.xyz/docs/get-started-for-programmers-1)
- [Lighter mainnet API endpoint](https://mainnet.zklighter.elliot.ai)
- [Lighter Python SDK](https://github.com/elliottech/lighter-python)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API calls and order placement guidance; live trading should use isolated credentials and explicit review.]

## Skill Version(s):

2.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
