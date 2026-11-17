## Description:

OKX Trader helps an agent maintain OKX grid trading strategies, generate trading reports, and record account snapshots for configured instruments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esojourn](https://clawhub.ai/user/esojourn)

### License/Terms of Use:

MIT

## Use Case:

Crypto trading operators and agent developers use this skill to monitor configured OKX instruments, maintain limit-order grid strategies, and capture daily account state. It is intended for users who understand exchange API permissions, automated order placement, and cryptocurrency trading risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically place and cancel real OKX orders, and server security evidence flags unsafe live-trading defaults and weak order-scope controls.

Mitigation: Use simulation mode first, keep OKX API keys trade-only with withdrawals disabled, and avoid enabling five-minute live maintenance until live opt-in, order ownership, and exposure-limit issues are fixed.

Risk: The local okx_data directory contains credentials, strategy settings, audit logs, and account snapshots.

Mitigation: Restrict filesystem access to okx_data and treat generated snapshots and configuration files as sensitive account data.

## Reference(s):

- [ClawHub OKX Trader skill page](https://clawhub.ai/esojourn/skills/okx-trader)
- [esojourn publisher profile](https://clawhub.ai/user/esojourn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown and console text from OKX reporting tools, plus JSON account snapshots and configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call OKX APIs, place or cancel orders, update grid_settings.json, and write snapshots under the local okx_data directory.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
