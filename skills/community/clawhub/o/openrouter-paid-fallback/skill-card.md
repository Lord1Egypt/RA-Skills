## Description:

Set OpenClaw to use a paid OpenRouter model first and fall back to free models when quota is exhausted or rate-limited.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h452624729](https://clawhub.ai/user/h452624729)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure OpenClaw model routing so a paid OpenRouter model is tried first and free fallback models are used when quota is exhausted or requests are rate-limited.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid primary OpenRouter model may incur charges.

Mitigation: Confirm the requested paid primary model and expected billing before changing routing.

Risk: Changing default model routing can affect all OpenClaw agents using the shared defaults.

Mitigation: Edit only the model-routing keys, preserve unrelated configuration, restart the gateway, and verify with openclaw status or /status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h452624729/skills/openrouter-paid-fallback)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Markdown with configuration keys and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to OpenClaw model routing changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
