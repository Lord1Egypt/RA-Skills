## Description: <br>
Perform a security audit of MCP servers to detect data exfiltration, command injection, permission escalation, and supply chain vulnerabilities before use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to audit MCP servers before installation or deployment. It guides source, network, file access, command execution, permission scope, and dependency review, then helps produce a risk-scored audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes intentionally dangerous code snippets and evil.com URLs as examples. <br>
Mitigation: Treat those snippets and URLs as illustrative audit patterns only; do not execute or adapt them outside a controlled review. <br>
Risk: Audit commands such as npm audit, pip-audit, grep, and git clone may be run against untrusted MCP server packages. <br>
Mitigation: Run review commands only for MCP servers selected for audit and prefer an isolated workspace when inspecting untrusted packages. <br>


## Reference(s): <br>
- [MCP Specification](https://modelcontextprotocol.io) <br>
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [CVE-2026-23744](https://nvd.nist.gov/vuln/detail/CVE-2026-23744) <br>
- [ClawHub skill page](https://clawhub.ai/aptratcn/mcp-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklist items, shell command examples, code snippets, and an audit report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only audit guidance; scanner evidence says dangerous snippets and evil.com URLs are examples only.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
