## Description:

Envoy (envoy.com). Use this skill for ANY Envoy request — searching and reading data. Whenever a task involves Envoy, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Envoy through an OOMOL-connected account can ask an agent to retrieve employee, sign-in flow, invite, and location records. The skill guides the agent to inspect each action's schema and return the result as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged unchecked CLI installation and the CLI's ability to change persistent agent skills.

Mitigation: Install and verify a specific CLI release before use, disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1, and connect only the intended Envoy account. Remote installer contents and hosted connector code remain outside the verified artifact.

## Reference(s):

- [Envoy API documentation](https://developers.envoy.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Envoy](https://envoy.com)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON results and shell commands described in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Envoy employee, flow, invite, and location lookups]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
