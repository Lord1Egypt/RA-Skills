## Description:

Helps agents use Gomboc.ai Community Edition to scan repositories and generate remediation reports or fix proposals for infrastructure, application, and configuration code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gomboc-ai](https://clawhub.ai/user/gomboc-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and security engineers use this skill to connect agent workflows to Gomboc.ai Community Edition for code issue scanning, remediation proposal generation, and CI/MCP integration guidance. It is intended for workflows where generated fixes are reviewed before committing or pushing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the local tools and deployment examples as overclaimed and under-scoped.

Mitigation: Review and tighten the integration before installation, including container/action version pinning and environment-specific configuration.

Risk: The MCP deployment example may expose a remediation service beyond the intended local development surface.

Mitigation: Bind MCP access to localhost or another explicitly trusted network boundary and remove automatic restart unless operationally required.

Risk: Authentication depends on a GOMBOC_PAT token used by local scripts, containers, and CI workflows.

Mitigation: Store the token in a proper secret manager, use a dedicated least-privilege token for each environment, and never commit it to source control.

Risk: Automated remediation workflows can create commits or pushes, and local CLI output may not prove that remediation occurred.

Mitigation: Require human review before commit or push workflows and validate remediation results through the connected Gomboc service or repository review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gomboc-ai/skills/gomboc-security-community)
- [Gomboc official documentation](https://docs.gomboc.ai)
- [Gomboc Community Edition signup](https://app.gomboc.ai)
- [Gomboc GitHub App](https://github.com/apps/gomboc-ai-community)
- [Gomboc community discussions](https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions)
- [Setup guide](references/setup.md)
- [MCP integration guide](references/mcp-integration.md)
- [GitHub Actions integration guide](references/github-action.md)
- [Security audit and practices](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, SARIF, code-oriented fix proposals, and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GOMBOC_PAT token and external Gomboc API access; remediation actions should be reviewed before commit or push.]

## Skill Version(s):

0.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
