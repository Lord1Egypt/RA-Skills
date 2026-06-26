## Description: <br>
Provides real-time quotes, technical and fundamental analysis, market sentiment, hot-sector tracking, trading strategy support, and price-alert guidance for mainland China A-share stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors and analysts use this skill to query and interpret mainland China A-share market data, individual stocks, market sentiment, sector momentum, and trading plans. It is intended for informational analysis and assistant-generated guidance, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Chinese finance data providers to retrieve market data. <br>
Mitigation: Install only when external finance-data requests are acceptable for the deployment environment. <br>
Risk: Trading suggestions may be incorrect, incomplete, or unsuitable for a specific user. <br>
Mitigation: Treat outputs as informational analysis rather than personalized financial advice, and require human review before acting. <br>
Risk: Price alerts can save user-supplied watchlist details locally. <br>
Mitigation: Avoid storing sensitive alert data and delete saved alert data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marjoriebroad/mar-a-stock-trading-assistant) <br>
- [Analysis methodology](references/analysis.md) <br>
- [Data sources](references/data-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, structured trading notes, risk warnings, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data source and fetch time when market data is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
