## Description: <br>
AI legal database search assistant for lawyers, judge assistants, and legal operations teams that helps retrieve statutes, verify cases, analyze similar cases, and generate interactive HTML legal analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal professionals use this skill to turn a legal question, case number, or matter description into structured legal search results, similar-case analysis, and an HTML report. It is intended for workflows that use user-configured Yuandian or PKULaw connectors, with a local demo mode for evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-configured legal data connectors require API keys or access tokens for third-party services. <br>
Mitigation: Confirm trust in the legal data providers before installation, keep secrets in MCP configuration only, and rotate tokens if they are exposed. <br>
Risk: Generated HTML reports may contain sensitive client, matter, or litigation records. <br>
Mitigation: Store, share, and delete generated reports according to confidentiality and records-retention requirements. <br>
Risk: Legal database results and AI case analysis can be incomplete or require jurisdiction-specific validation. <br>
Mitigation: Review the original statutes, case texts, and cited sources before relying on the report for legal work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/legal-search) <br>
- [Legal data source API guide](artifact/references/api-guide.md) <br>
- [Yuandian Open Platform](https://open.chineselaw.com/) <br>
- [PKULaw MCP](https://mcp.pkulaw.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown, HTML files] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration snippets, shell commands, structured legal analysis, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local legal_report_*.html or legal_report_demo.html files from structured legal search data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
