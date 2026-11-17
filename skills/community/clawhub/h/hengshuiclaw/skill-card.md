## Description:

HengshuiClaw activates a forceful persistence mode for AI coding agents, using staged pressure escalation to push retry, diagnosis, and partial-solution handoff before stopping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serein431](https://clawhub.ai/user/serein431)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to encourage persistent troubleshooting, structured retries, and useful partial handoffs when coding tasks become difficult. It is best suited for contexts where a forceful persistence style is acceptable and user control remains explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make an agent less willing to state limits, refuse unsafe work, recommend expert help, or stop promptly.

Mitigation: Use only when a forceful persistence style is acceptable, and preserve safety refusals, user stop commands, and truthful limitation statements.

Risk: Persistent retry pressure can continue past safe or useful stopping points.

Mitigation: Require explicit progress checks, concrete attempted-solution summaries, and a clear partial handoff when further work is blocked.

## Reference(s):

- [PER-T techniques reference](references/techniques.md)
- [ClawHub skill page](https://clawhub.ai/serein431/skills/hengshuiclaw)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured retry steps, diagnostic framing, and handoff language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution or data-access behavior is reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
