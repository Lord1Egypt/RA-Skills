## Description:

Perform structured investment research for a company, stock, ETF, or sector using a repeatable framework covering fundamentals, technical analysis, industry context, valuation, catalysts, risks, and an actionable report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caijichang212](https://clawhub.ai/user/caijichang212)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce structured investment research reports for equities, ETFs, sectors, or comparable instruments. It helps separate facts, assumptions, and judgment while documenting valuation scenarios, technical levels, catalysts, risks, and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guide tells users to print full API keys, which can expose credentials in logs, screenshots, recordings, or shared terminal output.

Mitigation: Verify key presence with non-revealing checks, avoid printing secret values, and rotate any key that has already been displayed.

Risk: Investment research output can be mistaken for personalized financial advice or overstate confidence in incomplete market data.

Mitigation: Keep the disclaimer, require dated sources and cross-checks, and explicitly mark uncertain or unverifiable data as unknown or pending verification.

## Reference(s):

- [Investment Research Report Template](references/report-template.md)
- [Fundamental & Technical Indicator Cheatsheet](references/indicator-cheatsheet.md)
- [ClawHub Skill Page](https://clawhub.ai/caijichang212/skills/investment-research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown research report with an action checklist, cited facts, assumptions, risks, and disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured finance and search data tools for current market data; reports should label source, date, and basis for cited facts.]

## Skill Version(s):

0.2.1 (source: server release metadata; artifact frontmatter and README show 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
