## Description:

Proactively captures reusable user preferences and prompts the agent to ask one brief, non-blocking follow-up when a future default would be useful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin010](https://clawhub.ai/user/wubin010)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent remember stable, non-sensitive preferences from direct sessions without blocking the current task. It is intended for preference-capture workflows where the agent asks concise follow-up questions and records confirmed defaults for future interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent behavior by adding Ask-to-Remember guidance to AGENTS.md or injecting bootstrap guidance through an OpenClaw hook.

Mitigation: Review the AGENTS.md and hook behavior before installation, and disable the optional hook if persistent startup injection is not desired.

Risk: The skill can store user-derived preferences and replies in MEMORY.md, atr-state.json, and atr-log.jsonl as plaintext.

Mitigation: Use it only for non-sensitive preferences, inspect these files regularly, and require explicit approval before writing durable memory.

Risk: Proactive preference questions may capture more user preference data than expected.

Mitigation: Keep questions low-friction and non-sensitive, honor refusals, and limit use to the user's direct main session.

## Reference(s):

- [ATR Test Scenarios](references/test-scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON state/log entries and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md, AGENTS.md, atr-state.json, and atr-log.jsonl; optional OpenClaw hook can inject bootstrap guidance.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
