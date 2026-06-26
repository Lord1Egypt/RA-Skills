## Description: <br>
Domain registrar and DNS manager using the Name.com CORE API for domain search, registration, DNS records, ACME DNS-01 challenges, and dynamic DNS updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patramsey](https://clawhub.ai/user/patramsey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill to let an agent search, buy, inspect, and manage Name.com domains and DNS records, including ACME DNS-01 and dynamic DNS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production Name.com credentials can allow real account, DNS, and purchase changes. <br>
Mitigation: Start with sandbox credentials, IP-whitelist tokens where possible, use account credit or payment limits, and require explicit confirmation before purchases, DNS deletions, DDNS updates, or nameserver changes. <br>
Risk: Installing and running the npm MCP server gives the package access to Name.com API credentials. <br>
Mitigation: Review the npm package before connecting production credentials and run the server in an isolated environment when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patramsey/namecom-registrar) <br>
- [Publisher Profile](https://clawhub.ai/user/patramsey) <br>
- [namecom-clawbot Repository](https://github.com/patramsey/namecom-clawbot) <br>
- [namecom-clawbot npm Package](https://www.npmjs.com/package/namecom-clawbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text responses with MCP tool results, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return domain availability, pricing, DNS record state, propagation status, confirmation tokens, and operational guidance.] <br>

## Skill Version(s): <br>
0.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
