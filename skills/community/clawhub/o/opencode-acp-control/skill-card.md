## Description:

Control OpenCode directly via the Agent Client Protocol (ACP). Start sessions, send prompts, resume conversations, and manage OpenCode updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjesuiter](https://clawhub.ai/user/bjesuiter)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to control OpenCode through ACP, including starting sessions, sending prompts, resuming conversations, reading responses, and checking update status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows an agent to start and control OpenCode sessions in a project workspace.

Mitigation: Install and use it only when that level of agent control over OpenCode and the target project is acceptable.

Risk: The update workflow can terminate running OpenCode processes.

Mitigation: Require explicit confirmation before killing processes and verify which OpenCode instances are affected.

Risk: The update guidance includes a remote installer command.

Mitigation: Avoid curl-to-bash installation and prefer a verified package manager or signed, pinned release update path.

## Reference(s):

- [Agent Client Protocol Docs](https://agentclientprotocol.com/llms.txt)
- [OpenCode ACP Skill GitHub Repository](https://github.com/bjesuiter/opencode-acp-skill)
- [OpenCode Releases](https://github.com/anomalyco/opencode/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON-RPC examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes polling guidance, session identifiers to track, resume workflow steps, and update workflow guidance.]

## Skill Version(s):

1.0.2 (source: release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
