## Description:

Diagnoses and tunes LLM providers (Groq, OpenRouter, Ollama), resolves rate limits/timeouts, and selects stable primary/fallback models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to triage OpenClaw LLM provider health, tune model routing, and recover from provider errors, rate limits, timeouts, or silent bot behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recovery playbook includes a session cleanup command that can delete main-agent session data without a backup or confirmation step.

Mitigation: Back up or quarantine session files first, identify the affected session, and require explicit operator confirmation before deleting session data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/neural-network-diagnostics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health report with inline shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports status, findings, actions applied, and one next verification step.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
