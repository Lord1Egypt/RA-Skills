## Description:

Generates JoinQuant backtest strategy code using six-part templates for cross-sectional multifactor stock selection and time-series technical timing with native JoinQuant APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to turn JoinQuant strategy requirements into backtest-ready Python code and API usage guidance for multifactor selection or technical timing strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategies include order-capable trading functions that could be adapted from backtests to simulated or live trading without sufficient audit.

Mitigation: Use generated strategies as backtest examples until they have been reviewed, tested, and deliberately adapted for the intended trading environment.

Risk: The skill recommends an undocumented JoinQuant content endpoint for API documentation lookup.

Mitigation: Confirm JoinQuant terms, authorization requirements, and rate limits before automating that endpoint; prefer official documentation or user-provided API references when required.

Risk: Incorrect factor names, IC direction, or get_price(panel=False) column handling can produce runtime errors or misleading strategy logic.

Mitigation: Cross-check factor metadata against JoinQuant sources and run small backtests before relying on generated code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxyzcyxpp/skills/joinquant-strategy-backtest)
- [JoinQuant API Access Pitfalls](references/joinquant-api-access-pitfalls.md)
- [Basic Strategy Template](templates/basic_strategy_template.py)
- [JoinQuant API documentation endpoint](https://www.joinquant.com/help/api/getContent?name=api)
- [JoinQuant API help](https://www.joinquant.com/help/api/help)
- [JoinQuant factor library](https://www.joinquant.com/view/factorlib/list)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python strategy code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated strategy code should be reviewed and adapted before simulation or live trading.]

## Skill Version(s):

0.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
