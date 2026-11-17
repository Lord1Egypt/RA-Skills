## Description:

Adds memory freshness warnings for OpenClaw 4.2 so agents verify older memory results before relying on them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicshliu](https://clawhub.ai/user/nicshliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add memory freshness reminders and verification steps when an agent relies on stored memories that may be stale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested edits to ~/.openclaw/openclaw.json can persistently change how OpenClaw treats memory in later sessions.

Mitigation: Review configuration changes before applying them and confirm they match the intended memory freshness policy.

Risk: Stored memory can become stale and lead an agent to use outdated file, function, or configuration details.

Mitigation: Verify memory-backed claims against current workspace files with grep, rg, or direct file reads before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicshliu/skills/openclaw-memory-freshness)
- [Publisher profile](https://clawhub.ai/user/nicshliu)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable code in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
