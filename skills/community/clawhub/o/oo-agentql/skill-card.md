## Description:

AgentQL (agentql.com). Use this skill for ANY AgentQL request — reading, creating, and updating data. Whenever a task involves AgentQL, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with an OOMOL-connected AgentQL account use this skill to query webpages, inspect account and session usage, and create Tetra browser sessions through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes downloaded CLI installers whose exact system changes were not inspected; setup can introduce broader persistent changes.

Mitigation: Review and approve CLI installation separately before fallback setup. Consider OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization, and preserve the skill's confirmation requirements for write actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [AgentQL](https://www.agentql.com)
- [AgentQL API reference](https://docs.agentql.com/rest-api/api-reference)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation; responses may include AgentQL data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
