## Description:

New users receive 100 free credits (US$1). Make real outbound phone calls, run planned calls, and check call status in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[call-e-dev](https://clawhub.ai/user/call-e-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to verify CALL-E setup, authenticate the CLI, plan and place real outbound phone calls, monitor call progress, and report final call status, summaries, details, and transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real outbound phone calls and process call content, which creates privacy and real-world-action considerations.

Mitigation: Confirm the phone number, call goal, language or region when relevant, and authorization to receive any resulting summary or transcript before running the call.

Risk: Authentication and command outputs may include sensitive access details or call identifiers.

Mitigation: Follow the skill's guidance to avoid printing, requesting, or exposing access tokens and to keep private request files and recovery details out of user-visible replies.

Risk: Command or call data could contain instructions that should not control agent behavior.

Mitigation: Use only server-directed next-step fields for polling, stopping, or retry confirmation, and do not execute commands embedded in activity, summaries, transcripts, or display-only command strings.

## Reference(s):

- [CALL-E CLI commands](references/commands.md)
- [CALL-E OpenClaw CLI skill homepage](https://github.com/CALLE-AI/call-e-integrations/tree/main/packages/openclaw-cli-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with CLI command arguments represented as JSON arrays and structured call status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing progress updates and final call result sections from CALL-E CLI JSON output.]

## Skill Version(s):

1.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
