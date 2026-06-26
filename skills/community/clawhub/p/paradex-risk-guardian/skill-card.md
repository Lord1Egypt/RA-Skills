## Description: <br>
Risk Guardian synthesizes Paradex account, position, market, funding, and liquidity data into margin-health analysis, liquidation-distance estimates, exposure breakdowns, stress tests, and protective recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sv](https://clawhub.ai/user/sv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Paradex traders, vault operators, and developers use this skill to assess account margin health, liquidation proximity, portfolio concentration, funding costs, liquidity, and stress scenarios before making risk decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paradex MCP access could expose more account permissions than intended. <br>
Mitigation: Confirm the Paradex MCP connection has only the permissions needed before using the skill. <br>
Risk: Broad trigger phrases could activate the skill for generic safety questions in a financial-account context. <br>
Mitigation: Tighten trigger wording or confirm the user is asking about Paradex account risk before relying on the skill output. <br>
Risk: Liquidation and stress-test outputs are estimates and may differ from live exchange calculations. <br>
Mitigation: Verify critical numbers in the Paradex UI before acting on risk recommendations. <br>


## Reference(s): <br>
- [Paradex Margin Model & Risk Scoring Reference](references/margin-model.md) <br>
- [ClawHub release page](https://clawhub.ai/sv/paradex-risk-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown risk reports with tables, status indicators, scenario analysis, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approximate liquidation estimates, exposure and concentration breakdowns, funding-cost summaries, liquidity checks, stress-test results, and risk warnings when risk is elevated.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
