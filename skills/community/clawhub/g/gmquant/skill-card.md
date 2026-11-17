## Description:

Chinese-language agent skill for building and running MyQuant gm.api quantitative trading strategy code, backtests, live or simulated runs, and market or account data queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turkeydick](https://clawhub.ai/user/turkeydick)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and quantitative traders use this skill to turn Chinese strategy descriptions into gm.api Python scripts, run backtests or live/simulated strategies, and query MyQuant market, account, and premium data APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles trading credentials unsafely.

Mitigation: Do not paste real tokens into chat, rotate any exposed token, use a least-privilege token where available, and pass credentials through an isolated environment.

Risk: Generated strategy code can run with broad local access.

Mitigation: Review generated strategy code before execution and run it in an isolated environment with a minimal allowlisted environment.

Risk: Live or simulated trading mode can place orders through the connected MyQuant environment.

Mitigation: Prefer backtesting first and avoid live mode until explicit safeguards, account selection, and strategy limits are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turkeydick/skills/gmquant)
- [turkeydick publisher profile](https://clawhub.ai/user/turkeydick)
- [MyQuant platform](https://www.myquant.cn)
- [Quick start](references/01-quick-start.md)
- [Core functions](references/02-core-functions.md)
- [Market data](references/04-market-data.md)
- [Order API](references/08-order-api.md)
- [Account query](references/10-account-query.md)
- [User guide](references/15-user-guide.md)
- [Premium data APIs](references/16-premium-data-apis.md)
- [Financial data fields](references/17-financial-data-fields.md)
- [Stock premium APIs](references/18-stock-premium-apis.md)
- [Fund premium APIs](references/19-fund-premium-apis.md)
- [Convertible bond premium APIs](references/20-cb-premium-apis.md)
- [Futures premium APIs](references/21-futures-premium-apis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce runnable gm.api strategy files and command-line invocations that require user-supplied credentials and a MyQuant terminal session.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
