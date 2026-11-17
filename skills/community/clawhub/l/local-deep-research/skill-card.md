## Description:

Performs multi-cycle, iterative deep research on complex topics using a local LDR service, providing detailed reports with citations and source tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eplt](https://clawhub.ai/user/eplt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to run quick summaries or detailed reports through a local LDR instance when they need comprehensive research with citations, literature reviews, competitive intelligence, or source-tracked analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script can execute assignments from a sourced LDR .env file.

Mitigation: Prefer environment variables, or verify that the LDR .env file is private and contains only trusted simple assignments before running the skill.

Risk: Credentials may be sent to an insufficiently constrained login URL.

Mitigation: Keep LDR_BASE_URL and LDR_LOGIN_URL on the same trusted local origin and use a dedicated low-privilege LDR account with a unique password.

Risk: The skill depends on a local service and shell/network permissions.

Mitigation: Run it only against an LDR service you control, ideally in a constrained environment with network access limited to the LDR host.

## Reference(s):

- [LDR API Reference](references/api.md)
- [LDR Skill Usage Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/eplt/skills/local-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON status/result objects, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running local LDR service, curl, jq, and local environment configuration for the service URL and optional credentials.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
