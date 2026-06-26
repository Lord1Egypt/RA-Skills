## Description: <br>
Complete guide to securing non-human identities in AI agent deployments, covering lifecycle management, credential rotation, workload identity federation, machine-to-machine authentication, governance, zero trust, and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and governance teams use this guide to design and review non-human identity controls for AI agent deployments. It focuses on credential lifecycle management, workload identity federation, machine-to-machine authentication, zero-trust enforcement, and compliance evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide references sensitive AGENT_SIGNING_KEY and STRIPE_API_KEY credentials that are not needed to install or read the guide. <br>
Mitigation: Use sandbox or test-scoped credentials only, and do not provide production signing, Stripe, Vault, OAuth, or cloud credentials to the skill installer or examples. <br>
Risk: Readers may adapt illustrative code examples into live environments without independently validating credential scope and execution behavior. <br>
Mitigation: Review and scan any adapted code before deployment, and validate permissions, credential rotation, and network access in a sandbox first. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mirni/greenhelix-nhi-security-agents) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown with Python examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference AGENT_SIGNING_KEY and STRIPE_API_KEY.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
