## Description: <br>
Automatically scans and generates deterministic, merge-ready code fixes for infrastructure, app code, and configs using Gomboc.ai's Open Remediation Language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gomboc-ai](https://clawhub.ai/user/gomboc-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan codebases, generate deterministic remediation proposals, and integrate code-fix workflows through CLI, MCP, GitHub Actions, or the Gomboc GitHub App. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support automated remediation flows that commit or push generated changes. <br>
Mitigation: Start with scan-only use and require pull request review before applying, committing, or pushing generated fixes. <br>
Risk: The skill depends on a Gomboc personal access token and sends repository-related scan context to Gomboc services. <br>
Mitigation: Store GOMBOC_PAT in a secret manager or CI secret, avoid literal tokens in shell profiles, and verify token scope before use. <br>
Risk: Persistent MCP and Docker-based workflows can keep the remediation service running longer than intended. <br>
Mitigation: Pin and verify Docker images, stop the MCP service when finished, and limit use to trusted repositories and environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gomboc-ai/gomboc-security-community) <br>
- [Gomboc documentation](https://docs.gomboc.ai) <br>
- [Open Remediation Language documentation](https://docs.gomboc.ai/orl) <br>
- [Gomboc GitHub App](https://github.com/apps/gomboc-ai-community) <br>
- [Gomboc community discussions](https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions) <br>
- [Setup guide](references/setup.md) <br>
- [MCP integration guide](references/mcp-integration.md) <br>
- [GitHub Actions integration](references/github-action.md) <br>
- [Security practices](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration snippets, JSON, Markdown, and SARIF remediation outputs depending on the selected command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gomboc personal access token and may call Gomboc APIs or local MCP workflows when the user enables those integrations.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
