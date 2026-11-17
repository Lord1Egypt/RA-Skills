## Description:

Helps developers choose a new npm dependency by comparing candidates or building a shortlist before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salemalem](https://clawhub.ai/user/salemalem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when deciding which new npm dependency to add. It compares named packages or builds a shortlist from a described need, then presents differences and a recommendation before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided descriptions may be sent to a third-party search service without warning.

Mitigation: Avoid including confidential descriptions and review the service’s data handling before using the skill with sensitive input.

Risk: The security scan was partial because several local references could not be resolved, so its evidence is incomplete.

Mitigation: Review the unresolved references and complete a security review before relying on the skill for sensitive package decisions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/salemalem/skills/npmscan-new-dependency-evaluation)
- [NPMScan MCP service](https://npmscan.com/api/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown comparison and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes package differences and provides a deterministic recommendation from current package data.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
