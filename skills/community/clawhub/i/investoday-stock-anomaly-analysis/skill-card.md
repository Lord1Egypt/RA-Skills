## Description: <br>
Analyzes unusual A-share stock moves by combining real-time quotes, index and sector context, news, announcements, and research sentiment into a structured attribution report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to ask why a Chinese A-share stock rose, fell, or moved intraday, and receive a structured report that separates market, sector, company-event, and institutional-sentiment drivers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake market-movement attribution for investment advice. <br>
Mitigation: Present the report as informational analysis only and avoid buy, sell, target-price, stop-loss, position-sizing, or timing recommendations. <br>
Risk: The analysis depends on current public market data from the investoday-finance-data dependency. <br>
Mitigation: Review the dependency separately and treat missing, stale, or unavailable data as insufficient evidence for a firm conclusion. <br>
Risk: Finance-related prompts may include unnecessary private account or trading details. <br>
Mitigation: Do not request or include private account details; keep the analysis limited to public market, company, and sector information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-anomaly-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured stock-movement attribution report with evidence windows, driver ranking, confidence language, and no trading advice.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
