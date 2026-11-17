## Description:

Opencli helps agents invoke a local OpenCLI installation for adapter discovery, browser-bridge health checks, Twitter/X routing, and external CLI passthrough with stable command patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Opencli to route tasks through existing OpenCLI adapters, retrieve structured output, check browser bridge health, and pass through supported external CLI commands when that is a better fit than browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can delegate to a mutable local source checkout or a PATH-resolved OpenCLI binary.

Mitigation: Install and run the skill only when the local OpenCLI checkout, update process, and fallback binary are trusted.

Risk: Browser-backed adapters and external CLI passthrough can act through logged-in accounts or affect local systems.

Mitigation: Use account- or system-impacting commands only with clear user intent and review commands before execution.

## Reference(s):

- [OpenCLI command cookbook](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/opencli)
- [Publisher profile](https://clawhub.ai/user/chaoyang78)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON output for agent use and returns exact commands when helpful for reuse.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
