## Description:

Connect to Pascal and use its MCP tools to create, inspect, edit, validate, save, or hand off editable 3D building scenes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aymericr](https://clawhub.ai/user/aymericr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect an MCP-capable host to Pascal, create or edit 3D building scenes, validate the scene, save supported changes, and return Pascal-provided editor links. It covers local projects, existing hosted workspaces, and explicitly authorized private agent-owned work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI setup can install mutable preview or beta packages that execute local code.

Mitigation: Review setup commands before running them, prefer a pinned Pascal CLI version or the documented preview archive, verify the stated SHA-256 directly, and avoid elevated installs.

Risk: Hosted Pascal API keys can grant access to a user's or organization's Pascal workspace.

Mitigation: Keep PASCAL_API_KEY in a secret manager or environment variable, do not print or commit it, and use only a key created for the intended workspace.

Risk: Autonomous registration creates a separate agent-owned Pascal account with its own projects and credential.

Mitigation: Register an autonomous account only after explicit user authorization, store the returned key securely, and explain that its projects do not automatically appear in another Pascal account.

Risk: Local Pascal CLI services can share active scene state across concurrent agent clients.

Mitigation: Use one active agent client per local service, save active work before updates or restarts, and use separate local data stores for independent concurrent work.

## Reference(s):

- [Pascal MCP developer documentation](https://editor.pascal.app/docs/developers/mcp)
- [Pascal connection and credential setup](artifact/references/setup.md)
- [Pascal MCP tool workflows](artifact/references/tool-workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, status summaries, and Pascal editor URLs when returned by tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should report validation checks, changed IDs, persistence evidence, unresolved issues, and unsupported deliverables without exposing API keys or local connector tokens.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata version 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
