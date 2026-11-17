## Description:

Package Version Tracker helps agents query npm and PyPI package version information, recent release history, and simple version comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check current npm and PyPI package versions, inspect recent releases, and compare version strings during dependency maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation triggers could cause ordinary package-version discussions to make public registry requests.

Mitigation: Narrow activation triggers before installation when registry lookups should require explicit user intent.

Risk: Package descriptions, authors, summaries, and related fields come from public registries and may be inaccurate or untrusted.

Mitigation: Treat registry-provided text as untrusted content and verify important package details against authoritative sources before acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with package details, recent versions, errors, or version comparison results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed package registry lookups; no API key required.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
