## Description:

Manage local Ollama models autonomously with health monitoring, automatic fallback, self-healing, and offline operation without internet dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[and-ray-m](https://clawhub.ai/user/and-ray-m)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage local Ollama model availability, health checks, fallback behavior, and recovery actions for offline-first agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows automatic service changes, cleanup, model reinstallations, and remote model fallback without clear consent or privacy boundaries.

Mitigation: Use it only with explicit approval for remote fallback and with policy controls that limit cleanup, restarts, and reinstallations to known Ollama paths.

Risk: Remote model fallback can conflict with offline-first or privacy-sensitive operation.

Mitigation: Disable remote fallback unless the request explicitly permits it and the data handling policy allows remote model use.

## Reference(s):

- [Offline Llama ClawHub skill page](https://clawhub.ai/and-ray-m/skills/offline-llama)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command names and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for health monitoring, local model fallback, service restarts, cache cleanup, and model reinstallations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
