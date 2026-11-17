## Description:

Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[164149043](https://clawhub.ai/user/164149043)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent operate MCP servers through the mcporter CLI, including listing tools, making calls, handling authentication, editing configuration, running daemon commands, and generating CLI or TypeScript interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad MCP administration actions, including authentication, configuration edits, daemon control, stdio commands, and arbitrary endpoint calls.

Mitigation: Use it only when those operations are explicitly requested, review sensitive commands before execution, and prefer a pinned and reviewed mcporter package version in higher-trust environments.

## Reference(s):

- [Mcporter Homepage](http://mcporter.dev)
- [ClawHub Skill Page](https://clawhub.ai/164149043/skills/mcporter-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill recommends JSON output from mcporter when machine-readable results are needed.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
