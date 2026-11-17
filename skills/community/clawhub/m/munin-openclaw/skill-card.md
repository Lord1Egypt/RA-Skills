## Description:

Munin provides persistent memory for OpenClaw agents through a CLI and MCP adapter connected to a configured Munin service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3d-era](https://clawhub.ai/user/3d-era)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add long-term agent memory backed by a configured Munin endpoint. It supports capability checks and memory actions through CLI or MCP-style execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may send agent context to the configured MUNIN_BASE_URL, and the included artifact does not contain the external Munin SDK/runtime packages needed to fully review data handling.

Mitigation: Install only if you trust Kalera/Munin, verify the resolved SDK/runtime package versions, and confirm encryption, retention, and deletion behavior before storing sensitive context.

Risk: Stored memories may include secrets or highly sensitive private context if the agent is allowed to persist unrestricted content.

Mitigation: Avoid storing secrets or sensitive private context until controls are verified, and scope project or Context Core IDs so memory is isolated to the intended use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3d-era/skills/munin-openclaw)
- [Munin service](https://munin.kalera.dev)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MUNIN_BASE_URL and optionally MUNIN_API_KEY to reach the configured Munin service.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
