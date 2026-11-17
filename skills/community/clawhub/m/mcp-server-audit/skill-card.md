## Description:

Audits MCP host configuration for exposed capabilities and configuration risks, then provides prioritized findings and hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review MCP host configuration before onboarding servers or troubleshooting agent capabilities. It summarizes each server's exposure and suggests practical configuration hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had partial coverage because three local references could not be resolved, and the skill reads host MCP configuration as part of its audit workflow.

Mitigation: Review the unresolved references and decide whether to allow local MCP configuration access before installing.

## Reference(s):

- [Project homepage](https://github.com/z-Zihan/awesome-skills)
- [ClawHub release page](https://clawhub.ai/z-zihan/skills/mcp-server-audit)

## Skill Output:

**Output Type(s):** [Security analysis, Markdown, Hardening guidance]

**Output Format:** [Markdown report with a server-by-server table, risk levels, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration values are redacted; environment and header key names may be reported.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
