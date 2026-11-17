## Description:

NadirClaw installs, configures, and runs an LLM routing proxy that routes prompts across providers to reduce AI API costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doramirdor](https://clawhub.ai/user/doramirdor)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install and configure NadirClaw as an LLM routing proxy for OpenClaw, Claude Code, or OpenAI-compatible tools, then monitor routing behavior and savings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer automatically installs an unpinned external package.

Mitigation: Use a pinned, reviewed NadirClaw package version in a virtual environment before running the skill.

Risk: OpenClaw routing changes may cause future prompts to pass through a local proxy and onward to selected model providers.

Mitigation: Confirm the onboarding config changes, provider routing behavior, and rollback steps before using the proxy.

Risk: The installer starts a detached local service that can continue handling prompts after setup.

Mitigation: Start the service manually when tighter operational control is needed and monitor or stop the process explicitly.

## Reference(s):

- [NadirClaw skill page](https://clawhub.ai/doramirdor/skills/nadirclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, local service startup, OpenClaw onboarding, provider routing configuration, and monitoring commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
