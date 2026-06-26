## Description: <br>
Agent Memory for Commerce helps developers build commerce agents that remember customers, maintain transaction state across sessions, and reconcile billing context at scale using tiered memory architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this guide to design commerce agents that preserve customer context, transaction state, payment memory, and reconciliation records across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide discusses commerce agents that can make purchases and handle wallet or payment state. <br>
Mitigation: Use sandbox or least-privilege credentials first, and require explicit approval gates before any real transaction or production payment credential is used. <br>
Risk: The examples reference customer memory, transaction history, and billing context that may include sensitive customer data. <br>
Mitigation: Define retention limits, deletion workflows, access controls, and redaction rules before applying the patterns to real customer data. <br>
Risk: The skill requires sensitive environment variables including GREENHELIX_API_KEY, WALLET_ADDRESS, and REDIS_URL. <br>
Mitigation: Store credentials in a managed secret store, scope them narrowly, and avoid exposing production values while reviewing or adapting the examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-memory-commerce) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guide with Python code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executing educational guide; examples reference GreenHelix credentials and Redis configuration.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
