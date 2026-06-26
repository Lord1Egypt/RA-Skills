## Description: <br>
Provides stock technical analysis, fundamental analysis, market sentiment assessment, and integrated trading guidance for investment decision support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Michael20070814](https://clawhub.ai/user/Michael20070814) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to analyze individual stocks, compare multiple tickers, review portfolio composition, and generate research-oriented trading signals from finance API data. Outputs should be treated as decision support, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested stock symbols or portfolio ticker lists to external finance and news APIs. <br>
Mitigation: Avoid entering sensitive portfolio details beyond the ticker symbols needed for the analysis. <br>
Risk: Generated buy, sell, stop-loss, take-profit, and position-size outputs may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as research support and review decisions with appropriate financial, legal, and risk controls. <br>


## Reference(s): <br>
- [Investment API Reference](artifact/Investment_API_Reference.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/Michael20070814/investment-advisor) <br>
- [Publisher Profile](https://clawhub.ai/user/Michael20070814) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON from local Node.js analysis scripts, typically converted by the agent into Markdown or text investment analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts support full, technical, fundamental, signal, portfolio, and compare modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
