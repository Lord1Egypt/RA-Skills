## Description:

Generate and security-scan OpenClaw SKILL.md files for skill creation, security vulnerability scanning, ClawHub skill auditing, and agent skill packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and skill users use this agent skill to generate OpenClaw SKILL.md files and to scan skill content for security risks before installation or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends pasted skill content and generation details to ToolWeb for API processing.

Mitigation: Use a dedicated API key and avoid submitting private or secret-bearing SKILL.md content unless it has been redacted.

Risk: Security scan results are third-party API output rather than a local independent audit.

Mitigation: Treat scan responses as advisory evidence and review findings before installation, release, or deployment.

Risk: Successful API calls are disclosed as billable operations.

Mitigation: Confirm API key ownership, account limits, and intended usage before running generation or scanning requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/openclaw-skill-tools)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and structured scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ToolWeb API responses and may include generated SKILL.md content, security findings, recommendations, curl commands, and setup guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
