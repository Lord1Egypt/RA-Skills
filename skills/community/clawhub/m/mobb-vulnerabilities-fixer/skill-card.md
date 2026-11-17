## Description:

Scan, fix, and remediate security vulnerabilities in a local code repository using Mobb MCP/CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathansantilli](https://clawhub.ai/user/jonathansantilli)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to scan local repositories, review Mobb vulnerability fixes, and apply approved remediation patches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository files selected for scanning can be sent to Mobb for vulnerability analysis.

Mitigation: Confirm the scan scope before use, remove secrets or regulated data, and prefer cached or summary-only workflows when a full scan is unnecessary.

Risk: Monitoring or auto-fix behavior may apply code changes automatically when auto-fix is enabled.

Mitigation: Keep auto-fix disabled unless unattended changes are intended, and review, test, and commit any applied fixes deliberately.

Risk: Authentication requires a Mobb account and locally configured API credentials or browser authorization.

Mitigation: Configure credentials locally, avoid sharing tokens in prompts or chat, and retry the browser login flow if authorization fails.

## Reference(s):

- [MCP Tools for Mobb Fixes](references/mcp-scan-fix.md)
- [Mobb Authentication and Login Flow](references/mobb-auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with summaries, tool parameters, and patch application guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vulnerability summaries, requested scan parameters, authentication guidance, and approved code patch outcomes.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
