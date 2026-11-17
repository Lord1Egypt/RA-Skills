## Description:

Helium 10 (helium10.com). Use this skill for ANY Helium 10 request — searching and reading data. Whenever a task involves Helium 10, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Helium 10 users can use this skill to discover available read-only tools and search or read data through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute downloaded CLI installation code, and automatic skill synchronization may make broader changes to installed agent skills.

Mitigation: Review the CLI release before installing it, require approval for software installation, and consider disabling automatic synchronization with OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [Helium 10 MCP documentation](https://kb.helium10.com/hc/en-us/articles/51580564409883-Getting-Started-with-Helium-10-MCP)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured JSON responses, summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live action schema; available skill actions are limited to read-only tool discovery and calls.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
