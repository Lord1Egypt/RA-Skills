## Description:

Cost-optimizing model router for OpenClaw that routes each request to the cheapest capable Claude model using weighted scoring and supports Anthropic directly or OpenAI and Google models through OpenRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuralshift1](https://clawhub.ai/user/neuralshift1)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to install and configure a local model-routing proxy for cost-aware LLM selection across cron jobs, subagents, background tasks, and other OpenClaw workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer creates and enables a persistent root-level systemd service.

Mitigation: Review the installer and service unit before execution; prefer a foreground or user-level service when possible and avoid unattended agent installation.

Risk: Provider API keys may be placed in the systemd unit or handled by the installer.

Mitigation: Use explicit credentials for the intended provider, restrict access to service files, and rotate keys if they may have been exposed.

Risk: Request content and routing signals can be exposed through logs or forwarding to configured provider endpoints.

Mitigation: Disable per-request logging for sensitive workloads and use only trusted HTTPS provider endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neuralshift1/skills/iblai-openclaw-router)
- [Iblai OpenClaw Router README referenced by skill](https://github.com/iblai/iblai-openclaw-router)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenRouter API base referenced by skill](https://openrouter.ai/api/v1)
- [ClawRouter weighted scoring inspiration referenced by README](https://github.com/BlockRunAI/ClawRouter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to install a localhost router, update OpenClaw model configuration, and verify health and routing stats.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
