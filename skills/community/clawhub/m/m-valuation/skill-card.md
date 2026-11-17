## Description:

M估值法 provides a five-step stock valuation workflow based on ROIC and CAPM, including screening, intrinsic value calculation, risk analysis, scenario analysis, and investment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oldhouse-g](https://clawhub.ai/user/oldhouse-g)

### License/Terms of Use:


## Use Case:

Investors, analysts, and agents use this skill to generate structured stock valuation reports for A-share and Hong Kong-listed companies. The workflow supports qualification screening, valuation parameter calculation, intrinsic value review, risk analysis, scenario analysis, and investment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes exposed Tavily and Tushare API credentials.

Mitigation: Remove embedded tokens before distribution and require users to configure their own API keys through a secure local environment.

Risk: Hong Kong stock analysis can rely on hardcoded financial assumptions.

Mitigation: Expose those assumptions clearly or replace them with sourced data before treating the output as financial analysis.

Risk: The skill produces investment guidance that may be incorrect or incomplete.

Mitigation: Verify all data sources, calculations, and conclusions independently before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oldhouse-g/skills/m-valuation)
- [Publisher profile](https://clawhub.ai/user/oldhouse-g)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text report with markdown-style sections and shell command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces financial analysis guidance that should be independently verified before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
