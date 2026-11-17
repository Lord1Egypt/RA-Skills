## Description:

On This Day MCP wraps byabbe.se/on-this-day for free, no-auth access to historical events, births, and deaths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect agents to a Pipeworx MCP server for retrieving On This Day events, births, and deaths without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm package with local user privileges.

Mitigation: Pin mcp-remote to an exact reviewed version before installing or running the skill.

Risk: Local environment variables may be exposed to tooling launched during setup.

Mitigation: Run the skill in a restricted environment without sensitive environment variables.

## Reference(s):

- [Pipeworx On This Day Pack](https://pipeworx.io/packs/onthisday)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-onthisday)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [Markdown instructions with JSON configuration and MCP tool responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides get_events, get_births, and get_deaths tools; no API key is required.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
