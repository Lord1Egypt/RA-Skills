## Description: <br>
Performs structured investment research for companies, stocks, ETFs, and sectors across fundamentals, industry context, valuation, technical analysis, catalysts, risks, and actionable reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CaiJichang212](https://clawhub.ai/user/CaiJichang212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to produce repeatable investment research reports, compare securities or sectors, and separate sourced facts from assumptions and judgments. It is intended as research support and not as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses finance and search data tools that may require API credentials. <br>
Mitigation: Use trusted qveris and Tavily credentials, keep API keys in environment variables, and do not print or share secrets. <br>
Risk: Investment research prompts may expose confidential portfolio, client, or trading strategy details to third-party data or search tools. <br>
Mitigation: Avoid submitting confidential financial information and review data-sharing constraints before using external tools. <br>
Risk: Generated reports can be mistaken for financial advice or may rely on stale or unverifiable market data. <br>
Mitigation: Treat outputs as research support, verify sources and dates, cross-check independent data sources, and preserve the skill's disclaimer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CaiJichang212/investment-research) <br>
- [Report template](references/report-template.md) <br>
- [Indicator cheatsheet](references/indicator-cheatsheet.md) <br>
- [Configuration guide](CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown research report with action checklist, cited facts, assumptions, judgments, risks, and disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include valuation ranges, bull/base/bear scenarios, technical levels, monitoring indicators, and tool configuration guidance.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata; artifact frontmatter reports 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
