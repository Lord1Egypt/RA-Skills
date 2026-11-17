## Description:

Automatically scan and deterministically fix security issues in Terraform, CloudFormation, Kubernetes YAML, and other code or configuration files using Gomboc.ai Community Edition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gomboc-ai](https://clawhub.ai/user/gomboc-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, security engineers, and infrastructure teams use this skill to scan codebases, generate remediation proposals, and integrate fixes through a local CLI, MCP service, or CI/CD workflow. Teams should review proposed changes before applying, committing, or pushing them to protected repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gomboc personal access token and can expose workspace contents to Gomboc services during scan or remediation workflows.

Mitigation: Use a narrowly scoped, revocable token, store it in a secret manager or CI secret store, and avoid persisting it in shell startup files.

Risk: The MCP integration runs an external Docker image and exposes a local service that can access the mounted workspace.

Mitigation: Run the MCP service only when the image and deployment path are trusted, bind it to localhost, and apply local access controls.

Risk: Auto-remediation, auto-commit, or auto-push workflows can change repository contents without sufficient review.

Mitigation: Use protected branches, pull-request review, and scan-only or proposal-only modes unless automated changes are explicitly approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gomboc-ai/skills/gomboc-security)
- [Setup Guide](references/setup.md)
- [MCP Integration Guide](references/mcp-integration.md)
- [GitHub Actions Integration](references/github-action.md)
- [Security Audit and Practices](SECURITY.md)
- [Gomboc Documentation](https://docs.gomboc.ai)
- [Project Repository Listed in Artifact Metadata](https://github.com/Gomboc-AI/gomboc-community-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, SARIF, code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply repository changes when remediation, commit, or push workflows are enabled.]

## Skill Version(s):

0.2.0 (source: server release metadata, artifact .clawhub.yml, changelog released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
