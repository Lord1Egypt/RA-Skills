## Description:

Scans and assesses MCP servers for vulnerabilities, insecure configurations, data exposure, and compliance with SOC 2, GDPR, and ISO 27001 standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and compliance teams use this skill to discover MCP servers in agent environments, assess security and configuration risks, and produce remediation and compliance reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad inspection of MCP-related configurations can expose secrets, credentials, or PII in generated reports.

Mitigation: Run scans only against an explicit scope, keep reports local, redact sensitive values before sharing, and rotate any credentials that appear in output.

Risk: The skill requests broad environment and configuration discovery without detailed output-handling safeguards.

Mitigation: Define target agents, configuration paths, and MCP servers before execution, then review findings before acting on remediation guidance.

## Reference(s):

- [Mcp Server Scanner on ClawHub](https://clawhub.ai/engsathiago/skills/mcp-server-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown report with inventory, severity-scored findings, remediation steps, and compliance status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive security findings, secrets, and PII locations; keep reports local and redact before sharing.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
