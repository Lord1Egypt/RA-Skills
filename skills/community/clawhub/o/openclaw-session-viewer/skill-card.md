## Description:

Generate an interactive HTML viewer for reviewing OpenClaw conversation sessions, including conversation history, tool calls, tool results, token usage, and debugging details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nan-wang](https://clawhub.ai/user/nan-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect OpenClaw session logs, review conversation history, analyze tool activity, and debug context or token usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exports sensitive session content, including messages, thinking blocks, tool arguments, tool results, token usage, cost, and model details.

Mitigation: Use it only for sessions that are acceptable to export, write output to a private path, and inspect or redact generated files before opening or sharing them.

Risk: The security summary identifies unsafe local HTML/JSON output with documented injection and temporary-file risks.

Mitigation: Review the generated artifact before use, avoid predictable shared temporary locations, and prefer restrictive file permissions and explicit opt-in controls for sensitive fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nan-wang/skills/openclaw-session-viewer)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [HTML viewer file, optional JSON export, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated viewer can contain full user messages, assistant responses, thinking blocks, tool arguments, tool results, token usage, cost, and model statistics.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
