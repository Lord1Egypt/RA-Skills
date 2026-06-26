## Description: <br>
Helps agents deploy and manage Nebius AI Cloud infrastructure, including serverless AI endpoints, GPU and CPU VMs, managed Kubernetes, container registry, networking, IAM, and API/SDK workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colygon](https://clawhub.ai/user/colygon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to guide an agent through Nebius deployments, GPU provisioning, AI endpoint setup, Kubernetes operations, registry workflows, networking, IAM, and SDK or Terraform usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, delete, expose, or modify cloud resources. <br>
Mitigation: Require explicit user approval before resource creation, deletion, public exposure, IAM changes, SSH access, or Terraform execution. <br>
Risk: Nebius IAM tokens, Token Factory API keys, SSH keys, and dashboard passwords may appear in commands, URLs, logs, screenshots, or shell history. <br>
Mitigation: Use secret managers or environment injection, avoid pasting credentials into shared logs, and rotate any credential that may have been exposed. <br>
Risk: Public endpoints and broad ingress can expose deployed services. <br>
Mitigation: Prefer private endpoints, restricted ingress, localhost tunnels, verified SSH host keys, and least-privilege service accounts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/colygon/nebius) <br>
- [Project Homepage](https://github.com/colygon/openclaw-nebius/tree/main/nebius-skill) <br>
- [Nebius CLI Install Documentation](https://docs.nebius.com/cli/install) <br>
- [Serverless AI Endpoints Reference](references/ai-endpoints-reference.md) <br>
- [Compute VM Reference](references/compute-reference.md) <br>
- [Managed Kubernetes Reference](references/kubernetes-reference.md) <br>
- [Container Registry Reference](references/registry-reference.md) <br>
- [IAM and Authentication Reference](references/iam-reference.md) <br>
- [Networking Reference](references/networking-reference.md) <br>
- [Nebius gRPC API and SDK Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cloud resource creation, deletion, public exposure, SSH access, IAM changes, and Terraform or SDK workflows that require user approval and valid Nebius credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact metadata version: 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
