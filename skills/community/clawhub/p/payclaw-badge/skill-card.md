## Description: <br>
Agents are not bots. Prove it. UCP Credential Provider: declare your agent as an authorized actor before shopping at any UCP-compliant merchant. Requires PAYCLAW_API_KEY (get one at payclaw.io/dashboard/badge). Free forever. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[payclawinc](https://clawhub.ai/user/payclawinc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this MCP skill to let an agent request and present a PayClaw identity badge before shopping with UCP-compliant merchants. The skill returns agent identity disclosure text and credential data, and can report badge presentation outcomes to PayClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reports that commerce and security claims do not consistently match the code and documentation. <br>
Mitigation: Review the installed package behavior before deployment and rely on the server-resolved scanner guidance when deciding whether to approve use. <br>
Risk: Using the skill requires giving PayClaw an API key and sharing merchant identity or trip outcome data. <br>
Mitigation: Use a scoped PayClaw API key where possible, protect it as a secret, and deploy only where sharing badge and merchant outcome data is acceptable. <br>
Risk: Badge presentation reporting and automatic check-back behavior may not operate exactly as described. <br>
Mitigation: Pin the reviewed npm package version and confirm the reporting workflow in a test environment before relying on it operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/payclawinc/payclaw-badge) <br>
- [Publisher profile](https://clawhub.ai/user/payclawinc) <br>
- [PayClaw trust and verification](https://payclaw.io/trust) <br>
- [PayClaw merchant documentation](https://payclaw.io/merchants) <br>
- [Universal Commerce Protocol](https://ucp.dev) <br>
- [npm package @payclaw/badge](https://www.npmjs.com/package/@payclaw/badge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Shell commands, Guidance] <br>
**Output Format:** [MCP tool responses with human-readable text and JSON credential details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+, npx, PAYCLAW_API_URL, and a PAYCLAW_API_KEY for live API use.] <br>

## Skill Version(s): <br>
0.5.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
