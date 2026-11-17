## Description:

Godot MCP Integration helps AI assistants connect to a local Godot MCP server to automate editor tasks such as scene creation, node manipulation, script editing, resource management, and project control.

This skill is for research and development only.

## Publisher:

[thb32133451](https://clawhub.ai/user/thb32133451)

### License/Terms of Use:

Non-commercial use license

## Use Case:

Developers and engineers use this skill to configure Godot MCP access for AI clients and to guide AI-assisted Godot editor workflows. It is suited to local project automation involving scenes, nodes, scripts, resources, filesystem actions, debugging, animation, physics, UI, and batch changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable third-party plugin code into a local Godot project.

Mitigation: Use it only in trusted projects, review the plugin source before enabling it, and pin the plugin to a specific commit or signed release where possible.

Risk: The skill enables AI-driven writes, overwrites, deletes, and batch modifications to project files.

Mitigation: Keep the project under version control with backups and require explicit approval before any destructive or broad file-changing action.

Risk: User-level MCP configuration can expose the Godot editor automation endpoint beyond the intended project.

Mitigation: Prefer project-level MCP configuration and connect only to the local endpoint for the active Godot project.

## Reference(s):

- [Godot MCP Integration on ClawHub](https://clawhub.ai/thb32133451/skills/godot-mcp)
- [Godot MCP API Reference](artifact/references/api-reference.md)
- [Godot MCP Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include MCP tool-call examples that write or modify local Godot project files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
