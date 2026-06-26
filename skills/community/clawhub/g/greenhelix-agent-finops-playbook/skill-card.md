## Description: <br>
A guide for implementing cost governance in multi-agent systems with per-agent wallets, budget caps, spend alerts, cost attribution, dashboards, API key isolation, and Python integration examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform teams use this guide to design cost controls for multi-agent systems, including budget enforcement, spending analytics, webhook alerts, and per-agent cost attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can affect live billing, webhook, and API-key state if run against production accounts. <br>
Mitigation: Use sandbox endpoints and test credentials first; confirm amounts, endpoints, key scopes, recipients, and rollback steps before any production use. <br>
Risk: The guide includes both sandbox and production-style endpoint examples. <br>
Mitigation: Verify the base URL and credential context before running any snippet, and keep exploratory testing isolated from live accounts. <br>
Risk: The skill references sensitive credentials for API authentication and agent signing. <br>
Mitigation: Store credentials in a secrets manager or protected environment variables, scope keys narrowly, rotate them regularly, and never commit them to source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-finops-playbook) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API documentation](https://api.greenhelix.net/docs) <br>
- [FinOps Foundation](https://www.finops.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide that references GREENHELIX_API_KEY and AGENT_SIGNING_KEY for user-supplied environments.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
