## Description: <br>
Connects OpenClaw agents to n8n workflows by generating webhook skills, routing agent API calls through credential-isolated n8n pipelines, supporting bidirectional Gateway ingress, deployment guidance, and ClawHub publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ktopper](https://clawhub.ai/user/Ktopper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, generate, validate, deploy, and publish OpenClaw-to-n8n integrations where n8n holds external service credentials and OpenClaw invokes controlled webhook or Gateway flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Powerful autonomous Gateway, memory, and workflow-generation patterns can trigger high-impact actions or broad data movement. <br>
Mitigation: Keep Gateway access on localhost or a private tunnel, narrow autonomous triggers and tool allowlists, and require human approval for shell and high-impact workflow actions. <br>
Risk: Unverified installers, images, or downstream automation components could introduce supply-chain risk. <br>
Mitigation: Pin and verify installers and container images before use. <br>
Risk: Cloud memory or embedding flows may process sensitive user data. <br>
Mitigation: Avoid cloud memory and embedding flows unless users have explicitly consented. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ktopper/openclaw-n8n-orchestrator) <br>
- [Deployment Reference: OpenClaw + n8n](artifact/references/deployment.md) <br>
- [OpenClaw Gateway API Reference](artifact/references/gateway-api.md) <br>
- [n8n-claw Architecture Reference](artifact/references/n8n-claw-architecture.md) <br>
- [ClawHub Publishing Reference](artifact/references/publishing.md) <br>
- [Security Reference: OpenClaw + n8n Credential Isolation](artifact/references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML frontmatter, shell or Node.js code blocks, Docker Compose configuration, and validation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw skill directory guidance and templates for n8n webhook, Gateway, deployment, security, and publishing workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
