## Description:

Use the mcporter CLI to list, configure, authenticate, and call MCP servers and tools directly over HTTP or stdio, including ad-hoc servers, config edits, and CLI or type generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[livvux](https://clawhub.ai/user/livvux)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage MCP server configuration, authenticate against MCP servers, call MCP tools, and generate CLI or type wrappers from an installed mcporter CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: mcporter can interact with MCP servers and tools that may access accounts, local files, or external services.

Mitigation: Before authentication, configuration changes, ad-hoc server use, or tool calls, confirm the selected MCP server, target tool, and the access or changes that tool can perform.

Risk: The skill depends on the mcporter CLI and Homebrew tap being trustworthy.

Mitigation: Install only after reviewing and trusting the mcporter project and the pdxfinder Homebrew tap.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/livvux/skills/mcporter-skill)
- [mcporter project homepage](https://github.com/pdxfinder/mcporter)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed mcporter CLI and configured MCP servers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
