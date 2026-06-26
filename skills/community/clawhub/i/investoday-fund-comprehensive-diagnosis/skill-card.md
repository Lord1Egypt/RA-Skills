## Description: <br>
Generates a structured public fund diagnosis report using Investoday financial data, covering returns, risk-return fit, holdings, fund manager profile, fees, and dividend characteristics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to analyze a public fund by name or six-digit fund code and produce a multi-section diagnosis across performance, risk, holdings, manager history, fees, dividends, and follow-up variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send the fund name or code and the original fund-related question to the Investoday data workflow. <br>
Mitigation: Avoid entering sensitive personal context, and confirm that the request is limited to public fund research before use. <br>
Risk: Ambiguous fund names or codes can lead to analysis of the wrong fund. <br>
Mitigation: Confirm the resolved fund name and six-digit code before relying on the generated report. <br>
Risk: Fund diagnosis output may be mistaken for personalized investment advice. <br>
Mitigation: Treat the report as informational research and validate conclusions against the user's investment goals, risk tolerance, and qualified advice where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-fund-comprehensive-diagnosis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown fund diagnostic report with structured sections and bullet-point findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes analysis date, data source, fund overview, return and risk assessment, holdings, manager evaluation, fees, dividends, summary findings, and follow-up variables.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
