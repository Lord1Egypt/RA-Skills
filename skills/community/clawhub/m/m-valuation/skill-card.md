## Description: <br>
M估值法 is a stock valuation skill that uses a five-step ROIC and CAPM framework to screen stocks, calculate valuation parameters, estimate intrinsic value, and summarize risks and scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oldhouse-g](https://clawhub.ai/user/oldhouse-g) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to run a structured stock valuation report for a supplied ticker and optional company name. It is intended to support financial analysis by combining market data lookups, ROIC qualification, CAPM-derived discount-rate calculations, intrinsic value estimates, risk checks, scenario analysis, and an investment suggestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill embeds third-party API credentials. <br>
Mitigation: Replace embedded tokens with user-provided configuration or environment variables before installation or execution. <br>
Risk: The security review says the skill relies on outbound financial lookups and external helpers that users cannot easily control. <br>
Mitigation: Review and approve external service use, dependencies, and network access before running the valuation workflow. <br>
Risk: The security review says some financial inputs may be placeholders or require clearer labeling. <br>
Mitigation: Verify all financial assumptions and source data before using the report for investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oldhouse-g/m-valuation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/oldhouse-g) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text report with valuation sections and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a stock ticker and optionally a company name; may depend on third-party financial data and search services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
