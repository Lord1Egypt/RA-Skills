## Description: <br>
A production-oriented KYA implementation playbook for agent identity binding, authority scoping, runtime behavioral monitoring, and tamper-evident audit trails for EU AI Act compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform teams use this guide to design KYA verification workflows for autonomous agents, including identity binding, authority scoping, behavioral monitoring, audit logging, and reputation scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production-facing examples cover payments, escrow, suspension, revocation, and signing credentials, and should not be treated as a safe drop-in pipeline. <br>
Mitigation: Use sandbox endpoints and test credentials first, validate the compliance, logging, reputation, and limit-enforcement code, and require human approval before live payment, escrow, suspension, or revocation actions. <br>
Risk: The guide references AGENT_SIGNING_KEY for cryptographic agent identity signing. <br>
Mitigation: Add explicit secret handling for signing keys and make identity and operator verification hard gates before any authority or SLA creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-kya-verification) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guide with Python code examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference AGENT_SIGNING_KEY for agent identity signing.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
