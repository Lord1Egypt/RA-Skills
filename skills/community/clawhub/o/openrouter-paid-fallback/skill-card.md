## Description: <br>
Set OpenClaw to use a paid OpenRouter model first and fall back to free models when quota is exhausted or rate-limited. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h452624729](https://clawhub.ai/user/h452624729) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw model routing so a paid OpenRouter primary model is tried first, with free fallback models available for quota exhaustion or rate limiting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The paid OpenRouter primary model can incur usage charges or encounter billing limits. <br>
Mitigation: Confirm OpenRouter billing limits before installation and keep previous model settings available for rollback. <br>
Risk: Prompts may be routed through OpenRouter and fallback providers. <br>
Mitigation: Enable the skill only when that provider-routing path matches the user's privacy and operational requirements. <br>
Risk: Changing OpenClaw default model routing can affect all agents that rely on the global defaults. <br>
Mitigation: Preserve unrelated configuration, restart the gateway, and verify the resulting model routing with `openclaw status` or `/status`. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h452624729/openrouter-paid-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with configuration keys and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Changes default OpenClaw model-routing settings and requires a gateway restart plus status verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
