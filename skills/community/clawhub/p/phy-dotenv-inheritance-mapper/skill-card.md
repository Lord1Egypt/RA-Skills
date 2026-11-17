## Description:

Maps a project's dotenv inheritance chain into a resolved view, showing which .env layer each variable comes from, what overrides what, conflicts across environments, missing .env.example entries, and code-referenced variables with no definition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit local environment configuration, compare dotenv override behavior across frameworks and environments, and identify missing, conflicting, undocumented, or unused variables before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and print full dotenv values, including real secrets, in generated reports.

Mitigation: Run it only on repositories where dotenv values are safe for the agent to inspect, redact production secrets before use, and avoid sharing generated reports that contain raw environment values.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [12-Factor App: Config](https://12factor.net/config)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-dotenv-inheritance-mapper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, inline shell commands, configuration snippets, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw environment variable values discovered in local dotenv files.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
