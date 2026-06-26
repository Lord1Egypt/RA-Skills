## Description: <br>
EU AI Act Compliance for Autonomous Agents provides a compliance toolkit for AI agent commerce, including EU AI Act risk classification, Annex IV technical documentation, cryptographic audit trails, liability-bounded escrow patterns, service contract templates, continuous compliance monitoring, and implementation checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and compliance teams use this guide to add EU AI Act-oriented risk classification, audit logging, escrow controls, contract terms, monitoring, and documentation patterns to autonomous agent commerce systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable examples can change GreenHelix accounts, escrows, disputes, webhooks, and monitoring state, with unclear sandbox versus production boundaries. <br>
Mitigation: Use the sandbox or least-privilege test credentials first, and require explicit human approval before escrow, registration, webhook, dispute, daemon, or production monitoring actions. <br>
Risk: The guide references sensitive credentials, including GREENHELIX_API_KEY and AGENT_SIGNING_KEY. <br>
Mitigation: Do not provide production signing keys casually; scope, protect, and rotate credentials before using any production-capable example. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mirni/greenhelix-agent-compliance-toolkit) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix A2A Commerce Gateway API](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown with Python examples, contract templates, checklists, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-installing guide; examples may require GREENHELIX_API_KEY and AGENT_SIGNING_KEY for authenticated GreenHelix workflows.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
