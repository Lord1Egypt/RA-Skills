## Description:

Control OpenCode directly via the Agent Client Protocol (ACP). Start sessions, send prompts, resume conversations, and manage OpenCode updates. Includes automatic recovery, stuck detection, and session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[studio-hakke](https://clawhub.ai/user/studio-hakke)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to operate OpenCode through ACP: start or resume sessions, send coding prompts, manage retries, monitor progress, and recover stalled local sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup commands can remove lock files for unrelated OpenClaw sessions.

Mitigation: Run in an isolated environment or revise cleanup to target only the exact current session before use.

Risk: The helper script outputs executable workflow text built from user-supplied values.

Mitigation: Treat generated commands and JSON-RPC payloads as untrusted data, and review quoting and arguments before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/studio-hakke/skills/opencode-acp-control-v2)
- [Publisher profile](https://clawhub.ai/user/studio-hakke)
- [GitHub URL from skill metadata](https://github.com/berriosb/Opencode-Acp-Control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown workflow guidance with shell commands and JSON-RPC snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate executable workflow text that should be reviewed before running.]

## Skill Version(s):

2.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
