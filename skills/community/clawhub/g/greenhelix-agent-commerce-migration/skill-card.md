## Description: <br>
A step-by-step guide for developers retrofitting existing REST APIs with agent commerce capabilities, including x402 payment patterns, authentication bridging, gradual migration, testing, rollback procedures, and performance comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API teams use this guide to assess existing REST endpoints and plan a gradual migration to agent-ready commerce, including payment verification, agent identity, structured discovery, and rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may be mistaken for ready-to-run production middleware. <br>
Mitigation: Treat the skill as implementation guidance, adapt the examples to the target system, and review them before enabling live payment verification or settlement. <br>
Risk: Payment and signing examples require sensitive credentials. <br>
Mitigation: Use sandbox or least-privilege credentials and do not hardcode or commit API keys or signing keys. <br>
Risk: Caller classification or payment handling changes could disrupt normal clients. <br>
Mitigation: Review caller classification, test human and agent request paths separately, and require explicit approval before activating live payment flows. <br>


## Reference(s): <br>
- [GreenHelix documentation](https://docs.greenhelix.net) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [x402 specification](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with illustrative code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; review examples before adapting them for production systems.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
