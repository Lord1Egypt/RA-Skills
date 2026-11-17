## Description:

Helps agents set up shared, persistent project memory through Lodekeep MCP across sessions and tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steve0no](https://clawhub.ai/user/steve0no)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users configure Lodekeep to retain decisions and project notes across agent sessions and MCP-compatible clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notes sent to cloud storage may expose sensitive information or persist beyond the current session.

Mitigation: Do not put secrets, credentials, private customer data, or sensitive business details in notes unless their storage and retention are acceptable.

Risk: Persistent notes may influence later agent decisions after their underlying information changes.

Mitigation: Check note provenance against the current project revision before acting on recalled decisions.

## Reference(s):

- [Lodekeep skill on ClawHub](https://clawhub.ai/steve0no/skills/lodekeep)
- [Lodekeep](https://lodekeep.com)
- [Lodekeep project dashboard](https://lodekeep.com/app/projects)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Text]

**Output Format:** [Markdown guidance, configuration JSON, and memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-scoped recall requires projects to be included in the dashboard.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
