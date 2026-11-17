## Description:

Turn a day of memory into a clear owner brief with highlights, decisions, open loops, and next-step recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asistent-alex](https://clawhub.ai/user/asistent-alex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn daily memory files and optional lossless-claw SQLite messages into owner-facing briefs with highlights, decisions, open loops, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local OpenClaw memory and summarize potentially sensitive daily context.

Mitigation: Use --session-key with --use-lcm, keep memory sources narrowly scoped, and inspect generated briefs before sharing them.

Risk: The skill can write files and optionally send generated summaries by email.

Mitigation: Prefer file output for review first, verify recipients and message content before live sends, and enable email delivery only when needed.

Risk: The artifact includes unrelated GraQle agent-routing instructions.

Mitigation: Remove or ignore CLAUDE.md if those instructions should not affect agent tool routing in the installation environment.

## Reference(s):

- [Openclaw Mindkeeper on ClawHub](https://clawhub.ai/asistent-alex/skills/openclaw-mindkeeper)
- [Publisher profile](https://clawhub.ai/user/asistent-alex)
- [Firma de AI](https://firmade.ai)
- [Firma de IT](https://firmade.it)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or HTML brief, with optional output files and email message output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run locally from the Node CLI, read markdown memory files, optionally read lossless-claw SQLite messages, and optionally write or send generated briefs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
