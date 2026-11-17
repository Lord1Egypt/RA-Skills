## Description:

Professional quantitative trading system for cryptocurrency - backtesting, paper trading, live trading, and strategy optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading-system operators use this skill to guide OpenClaw agents through cryptocurrency strategy backtesting, optimization, paper trading, and live-trading workflows. It produces commands, configuration, and implementation guidance that should be reviewed before any market execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package mixes the crypto trading skill with an unrelated video-generation skill.

Mitigation: Use only the quant documentation unless the publisher fixes or removes the unrelated English video-generator file.

Risk: The skill asks users to install mutable external code while handling API keys.

Mitigation: Install in an isolated environment, pin and inspect the exact repository commit, avoid global installs, and keep API keys out of shell history and chats.

Risk: The skill documents live trading workflows that can place real exchange orders.

Mitigation: Disable withdrawals on exchange keys, prefer testnet or paper trading, and require explicit confirmation before any live trading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/openclaw-quant-skill)
- [Openclaw Quant Project Documentation](https://github.com/ZhenRobotics/openclaw-quant)
- [Openclaw Quant Issues](https://github.com/ZhenRobotics/openclaw-quant/issues)
- [Openclaw Quant Discussions](https://github.com/ZhenRobotics/openclaw-quant/discussions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading workflow guidance and risk warnings for paper or live trading.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
