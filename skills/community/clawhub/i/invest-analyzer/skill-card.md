## Description: <br>
Invest Analyzer guides an agent through public-equity screening, FCF valuation, investment-style classification, and decision reporting using public filings and financial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litousteven](https://clawhub.ai/user/litousteven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to screen A-share and Hong Kong public equities, structure FCF and owner-earnings calculations, classify investment styles, and produce human-reviewable investment research reports. It is intended to support research workflows, not replace verification against official filings or professional judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rely on web search, downloaded filings, PDF parsing, and an optional Baidu search key to gather financial data. <br>
Mitigation: Review and configure the referenced search, browser, and PDF skills separately; protect any key file with restrictive permissions. <br>
Risk: Investment conclusions can be wrong if public data is stale, parsed incorrectly, or taken from lower-authority sources. <br>
Mitigation: Verify key figures against official filings or investor-relations documents before acting, and treat generated conclusions as research support rather than investment advice. <br>


## Reference(s): <br>
- [Invest Analyzer ClawHub Page](https://clawhub.ai/litousteven/invest-analyzer) <br>
- [Publisher Profile](https://clawhub.ai/user/litousteven) <br>
- [Invest Analyzer README](README.md) <br>
- [investTemplate V5.5.6](https://github.com/sunheyi6/investTemplate) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with tables, formulas, risk notes, and occasional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite data source tiers, preserve calculation assumptions, and state that investment conclusions require human verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
