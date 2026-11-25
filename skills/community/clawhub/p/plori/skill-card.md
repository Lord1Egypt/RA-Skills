## Description:

Runs tasks on Plori cloud agents that continue after the chat ends, such as background or parallel builds, programs for recurring work, long jobs and research saved as files. Not for quick tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchen-plori](https://clawhub.ai/user/yuchen-plori)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to Plori and manage cloud workspaces for long-running or parallel tasks, saved research, and recurring programs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because it recommends remote installer scripts and an unpinned CLI package, and one scanner’s inspection was partial.

Mitigation: Verify the installer and CLI package source and version before installation; treat the scan results as incomplete risk coverage.

## Reference(s):

- [Plori MCP connection guide](https://plori.ai/mcp)
- [Plori integration entry point](https://plori.ai/agents.md)
- [Plori CLI documentation](https://plori.ai/docs/cli)
- [Plori CLI package](https://www.npmjs.com/package/@plori/cli)
- [Plori authentication details](https://plori.ai/auth.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for connecting to Plori and operating cloud workspaces, agents, and scheduled work]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
