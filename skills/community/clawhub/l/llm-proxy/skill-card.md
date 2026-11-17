## Description:

Provides a local LLM API proxy for routing requests to multiple configured providers with content audit rules, health checks, logging, and service control commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[394286006](https://clawhub.ai/user/394286006)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to start, stop, monitor, and configure a local LLM API proxy that forwards LLM requests to selected providers while applying configurable content audit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy forwards prompts and API credentials to whichever providers are configured.

Mitigation: Review provider configuration and credentials before use, and keep the service bound to 127.0.0.1 unless a separate network security review approves another binding.

Risk: The control script can terminate unrelated local processes on the configured port.

Mitigation: Inspect the configured port and owning process before running start, stop, or restart, and avoid running the control script as root.

Risk: The advertised safety filter has bypasses and should not be treated as a security boundary.

Mitigation: Use it only as an advisory content audit layer until PID handling, port-kill behavior, streaming filtering, whitelist logic, and thread limiting are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/394286006/skills/llm-proxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also surface local service health or status JSON when proxy control commands are run.]

## Skill Version(s):

1.0.4 (source: server release evidence, released 2026-03-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
