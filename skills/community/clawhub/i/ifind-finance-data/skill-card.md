## Description: <br>
iFinD (同花顺) financial data query skill for stocks, funds, macroeconomic and industry data, financial news, and announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and finance data users use this skill to query iFinD MCP services for stock, fund, macroeconomic, industry, news, and announcement data. It helps compose calls, configure the iFinD auth token, and interpret JSON responses from the helper clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper clients disable HTTPS certificate validation while sending an iFinD auth token to a remote API. <br>
Mitigation: Review before installing and use a real token only after the helper clients are edited or wrapped to validate TLS certificates. <br>
Risk: Broad finance-related triggers may cause this provider to be used for ordinary finance queries. <br>
Mitigation: Limit use to explicit iFinD or 同花顺 finance-data requests and review returned data before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/ifind-finance-data) <br>
- [iFinD homepage](https://www.51ifind.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline code examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided iFinD auth token; helper clients call remote iFinD MCP endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
