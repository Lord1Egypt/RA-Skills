## Description: <br>
Automatically scan and deterministically fix security issues in Terraform, CloudFormation, Kubernetes YAML, configuration files, and other code using Gomboc.ai Community Edition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gomboc-ai](https://clawhub.ai/user/gomboc-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security engineers, and infrastructure teams use this skill to scan repositories, generate deterministic remediation output, and apply or review fixes through a CLI, MCP server, or CI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remediation workflow can apply, commit, and push repository changes. <br>
Mitigation: Run scan and fix-generation modes first, use a dedicated branch, inspect diffs, and avoid unattended push workflows. <br>
Risk: The skill requires a Gomboc personal access token for API access. <br>
Mitigation: Store GOMBOC_PAT as a scoped secret, protect it from logs and shell history, rotate it when needed, and grant only the access required for the repositories being scanned. <br>
Risk: Repository content and findings are handled through Gomboc services during scan and fix workflows. <br>
Mitigation: Install and run the skill only for repositories you are willing to trust to Gomboc's service, and confirm data-handling expectations before using it on sensitive code. <br>
Risk: The optional MCP integration runs the gombocai/mcp:latest container persistently. <br>
Mitigation: Pin the container image to an audited version or separately audit it before long-running use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gomboc-ai/gomboc-security) <br>
- [Setup guide](references/setup.md) <br>
- [MCP integration guide](references/mcp-integration.md) <br>
- [GitHub Actions integration](references/github-action.md) <br>
- [Security audit and practices](SECURITY.md) <br>
- [Gomboc documentation](https://docs.gomboc.ai) <br>
- [Gomboc community support](https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON, SARIF, shell commands, and generated code fixes depending on command and integration mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOMBOC_PAT for API access; remediation commands can optionally commit or push repository changes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata, .clawhub.yml, README badge, CHANGELOG entry dated 2026-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
