## Description:

Bootstraps a fresh OpenClaw install into a reliable execution agent by aligning model routing, gateway tokens, anti-stall behavior, autonomy checks, and verification gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure a new OpenClaw instance for more consistent task execution, provider routing, gateway access, anti-stall behavior, and setup verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes token audit guidance that can print gateway tokens in plaintext.

Mitigation: Do not run token-printing audits as written; check token presence and equality without exposing secret values in logs or chat.

Risk: The skill proposes persistent agent behavior files, memory rules, and scheduled jobs.

Mitigation: Require explicit approval before AGENTS.md, HEARTBEAT.md, memory-rule, cron, or event-schedule changes; define scope, expiration, safe logging, and removal steps.

Risk: Model routing and gateway token changes can break access if applied incorrectly.

Mitigation: Back up configuration before edits, keep one source of truth, restart services deliberately, and verify model and gateway access before considering setup complete.

## Reference(s):

- [OpenClaw Growth Pack examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/dalomeve/skills/openclaw-growth-pack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rollback and verification checklists; scheduled work, memory rules, and persistent agent behavior require explicit review before use.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
