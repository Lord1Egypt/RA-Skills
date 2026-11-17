## Description:

Audit a project's npm dependencies for known vulnerabilities and risky install scripts before installing, upgrading, or shipping. Use when the user pastes or attaches a package.json/lockfile, lists dependencies, or asks to check/audit/scan their packages for security issues — including comparing two snapshots (a PR diff) or checking license compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salemalem](https://clawhub.ai/user/salemalem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to audit npm dependency inventories for known vulnerabilities, risky install scripts, maintenance signals, and license issues, and to compare snapshots or prioritize fixes. It queries package information through the npmscan service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency inventories may contain private project information and are sent to an external service for analysis.

Mitigation: Review data-sharing requirements and submit only inventories approved for external processing; remove sensitive project details where possible.

Risk: The security review is incomplete: obfuscated instruction text could not be fully evaluated and some references were unresolved.

Mitigation: Review the skill and unresolved references before deployment, and treat the scan assessment as incomplete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/salemalem/skills/npmscan-dependency-audit)
- [Publisher profile](https://clawhub.ai/user/salemalem)
- [npmscan MCP server](https://npmscan.com/api/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown report with package findings, summaries, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the supplied inventory and available package data.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
