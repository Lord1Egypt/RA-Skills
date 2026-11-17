## Description:

Lorem MCP wraps loripsum.net to generate lorem ipsum text without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to a remote Pipeworx lorem-ipsum MCP service and generate placeholder text through the exposed paragraph generation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup command runs an npm package and connects to Pipeworx's remote MCP service.

Mitigation: Install and run it in an environment without unnecessary secrets or file access.

Risk: The documented mcp-remote bridge uses an unpinned latest version.

Mitigation: Prefer a pinned mcp-remote version or a locked installation where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-lorem)
- [Pipeworx Lorem pack](https://pipeworx.io/packs/lorem)
- [Pipeworx](https://pipeworx.io)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text from MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is documented.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
