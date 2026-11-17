## Description:

Helps agents deploy and manage Nebius AI Cloud infrastructure, GPU resources, Kubernetes clusters, serverless endpoints, registries, IAM, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colygon](https://clawhub.ai/user/colygon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to guide agent-assisted deployment and management of Nebius cloud services, including GPU VMs, serverless AI endpoints, managed Kubernetes, container registries, networking, IAM, SDKs, and Terraform-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact creation, update, deletion, and exposure of Nebius cloud resources.

Mitigation: Require explicit user confirmation before create, update, delete, or public exposure commands, and prefer list-or-check steps before creating resources.

Risk: The artifact includes a curl-to-bash CLI installation path.

Mitigation: Avoid that installer unless it is independently verified; prefer a trusted package or manually reviewed installation method.

Risk: IAM tokens, API keys, dashboard passwords, and provider tokens may be handled during deployment workflows.

Mitigation: Use a secret manager or ephemeral secure input, and avoid placing secrets in chat, shell history, logs, or persistent environment variables.

Risk: Generated endpoint and dashboard workflows may expose services through public IPs or plaintext links.

Mitigation: Keep endpoints private or authenticated, use SSH tunnels or HTTPS where appropriate, and avoid exposing dashboards directly over plaintext public links.

Risk: Container images, plugins, and SSH connections can introduce supply-chain or host-authenticity risk.

Mitigation: Pin images and plugins to trusted versions or digests and verify SSH host keys before connecting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colygon/skills/nebius)
- [OpenClaw Nebius source homepage](https://github.com/colygon/openclaw-nebius/tree/main/nebius-skill)
- [Nebius CLI install documentation](https://docs.nebius.com/cli/install)
- [Serverless AI Endpoints Reference](artifact/references/ai-endpoints-reference.md)
- [Compute VM Reference](artifact/references/compute-reference.md)
- [Managed Kubernetes Reference](artifact/references/kubernetes-reference.md)
- [IAM & Authentication Reference](artifact/references/iam-reference.md)
- [Nebius gRPC API & SDK Reference](artifact/references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks, configuration snippets, and JSON-oriented CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that create, update, delete, or expose cloud resources and should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata version 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
