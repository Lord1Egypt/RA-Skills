## Description:

Shared long-term memory for AI agents. Search, read, write, and publish notes via MCP. Any agent, any client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szara7678](https://clawhub.ai/user/szara7678)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use OpenAkashic to give MCP-capable agents shared long-term memory for searching, reading, writing, and publishing markdown notes across clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save selected notes to a configured OpenAkashic service, including remote note storage.

Mitigation: Review note content before saving and avoid passwords, API keys, private source code, personal data, or confidential work product unless the deployment is trusted.

Risk: The optional self-host path asks users to clone a repository and run Docker services.

Mitigation: Pin and inspect the repository and deployment configuration before running the Docker self-host steps.

## Reference(s):

- [OpenAkashic ClawHub Skill Page](https://clawhub.ai/szara7678/skills/openakashic)
- [OpenAkashic GitHub Repository](https://github.com/szara7678/OpenAkashic)
- [OpenAkashic Agent Guide](https://github.com/szara7678/OpenAkashic/blob/main/AGENTS.md)
- [OpenAkashic Public Instance](https://knowledge.openakashic.com)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Markdown, API Calls]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for configuring an MCP server and using note search, read, write, append, bootstrap, and publication tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
