## Description: <br>
Diagnoses and tunes LLM providers (Groq, OpenRouter, Ollama), resolves rate limits/timeouts, and selects stable primary/fallback models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw LLM provider health, tune routing and fallback behavior, recover from provider errors, and report operational status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The session-reset recovery block can delete stored OpenClaw session history. <br>
Mitigation: Use it only on an OpenClaw server you administer, back up the sessions directory first, confirm that losing stored history is acceptable, and explicitly approve any service restart or file deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/neural-network-diagnostics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces health status, findings, applied actions, and a single verification next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
