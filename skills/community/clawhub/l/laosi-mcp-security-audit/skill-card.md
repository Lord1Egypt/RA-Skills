## Description:

Performs comprehensive security audits on MCP servers including vulnerability scans, malware detection, compliance checks, and detailed remediation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan MCP server or skill directories for vulnerable patterns, suspicious code, compliance issues, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads source and configuration files under the directory selected by the user, which may include sensitive project data.

Mitigation: Run it only against the specific MCP server or skill folder intended for audit, not a home directory or unrelated private workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-mcp-security-audit)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON reports and human-readable terminal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity counts, score, grade, detailed findings, and prioritized recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
