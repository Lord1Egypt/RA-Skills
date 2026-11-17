## Description:

Security audit for MCP (Model Context Protocol) servers that helps detect data exfiltration risks, command injection, permission escalation, and supply chain vulnerabilities before adding MCP servers to an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to review MCP servers before adoption, focusing on source trust, network behavior, file access, command execution, permissions, and dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the checklist as an automated security verdict.

Mitigation: Use it as review guidance and independently validate findings before approving or rejecting an MCP server.

Risk: Suggested shell commands inspect target MCP code and dependency manifests.

Mitigation: Run commands only against MCP code you intend to review and evaluate command output before taking action.

Risk: External incident or CVE references may influence adoption decisions.

Mitigation: Verify external vulnerability and incident claims independently when they affect a security decision.

## Reference(s):

- [MCP Specification](https://modelcontextprotocol.io)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CVE-2026-23744](https://nvd.nist.gov/vuln/detail/CVE-2026-23744)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with audit checklists, shell command examples, risk scoring, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no bundled executable code.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
