## Description: <br>
Find the cheapest way to send money between any two currencies. Compares 22+ crypto exchanges and 19 remittance providers in real-time. Free, open source, no affiliate fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miguelvalenciav](https://clawhub.ai/user/miguelvalenciav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Money Router to compare cross-border transfer options, request ranked routes, and receive provider paths, fees, rates, and step-by-step sending instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quote and rate-verification requests send transfer parameters and observed-rate details to Coinnect. <br>
Mitigation: Submit only non-sensitive quote parameters and avoid personal, account, or transaction-identifying details. <br>
Risk: Optional API keys and MCP or self-hosted usage can expose credentials or run third-party code. <br>
Mitigation: Keep API keys private and review the external Coinnect package before running the optional MCP server or self-hosted code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/miguelvalenciav/money-router) <br>
- [Coinnect Homepage](https://coinnect.bot) <br>
- [Coinnect API Documentation](https://coinnect.bot/docs) <br>
- [Coinnect Whitepaper](https://coinnect.bot/whitepaper) <br>
- [Coinnect Repository](https://github.com/coinnect-dev/coinnect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API request examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include quote parameters, ranked route details, provider paths, fee and rate breakdowns, and optional MCP setup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
