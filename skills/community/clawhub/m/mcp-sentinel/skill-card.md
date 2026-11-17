## Description:

Audits MCP and AI agent configuration files for risky commands, broad filesystem access, inline secrets, and prompt-injection risks, then reports findings by severity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fasjdas](https://clawhub.ai/user/fasjdas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to run or interpret MCP Sentinel audits on MCP and AI agent configuration files, prioritize risky command, filesystem, secret, and prompt-injection findings, and guide remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to install and run mutable third-party code without pinned release or provenance verification.

Mitigation: Install only after choosing a reviewed commit or release and verifying provenance.

Risk: Running the scanner against broad directories can expose unrelated files or secrets to the audit process.

Mitigation: Run in a sandbox or container with read-only access to the specific project being audited.

Risk: Static scanner findings are best-effort signals and may miss issues or flag benign configuration.

Mitigation: Treat findings as prompts for human review and remediation rather than as a complete security review.

## Reference(s):

- [MCP Sentinel ClawHub listing](https://clawhub.ai/fasjdas/skills/mcp-sentinel)
- [MCP Sentinel repository linked by the skill](https://github.com/fasjdas/mcp-sentinel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with command snippets and optional JSON audit output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should be summarized by severity, and secret values should be redacted.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
