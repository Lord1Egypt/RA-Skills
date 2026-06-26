## Description: <br>
Investment Research OS coordinates specialist analyst prompts and a CIO decision layer to produce source-traceable investment research, valuation scenarios, red-team risk analysis, and position guidance for single or comparative equity targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunhe-8922](https://clawhub.ai/user/sunhe-8922) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to transform an investment question into a structured research workflow covering industry state, company quality, financials, valuation, expectation gaps, red-team risks, and CIO-style decision guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment research outputs may be mistaken for financial advice or relied on without independent review. <br>
Mitigation: Treat outputs as research support only, verify conclusions against authoritative sources, and require human review before investment decisions. <br>
Risk: The skill uses external financial and web data sources whose availability, freshness, or accuracy can vary. <br>
Mitigation: Check source URLs, coverage periods, and verification notes for each data point, and cross-check critical facts before using the report. <br>
Risk: Research runs on sensitive targets may save local report files. <br>
Mitigation: Use explicit prompts or confirmations before full research on sensitive targets and review generated files before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunhe-8922/investment-research-os) <br>
- [Macrotrends financial history template](https://www.macrotrends.net/stocks/charts/{TICKER}/{slug}/{metric}) <br>
- [StockAnalysis forecast template](https://stockanalysis.com/stocks/{TICKER}/forecast/) <br>
- [OpenAlex works API template](https://api.openalex.org/works?filter=...) <br>
- [World Bank indicators API template](https://api.worldbank.org/v2/country/{code}/indicator/{id}) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research reports with source tables, checklists, valuation scenarios, risk sections, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved under research/{target}_{date}.md or research/portfolio_{date}.md when the host agent has local file-write capability.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
