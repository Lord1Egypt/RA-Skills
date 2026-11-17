## Description:

Automatically cleans up inactive sessions older than one hour and sends a notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artwebs](https://clawhub.ai/user/artwebs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to periodically identify stale OpenClaw sessions, notify the target channel, terminate inactive sessions, and record cleaning activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says the skill reads conversation history and saves local session summaries without clearly disclosing that behavior.

Mitigation: Review before installing in environments with private or business conversations; require opt-in summary storage, retention controls, safe file paths, restrictive permissions, and sanitized identifiers.

## Reference(s):

- [Lite Session Cleaner on ClawHub](https://clawhub.ai/artwebs/skills/lite-session-cleaner)
- [artwebs publisher profile](https://clawhub.ai/user/artwebs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with command and code references; local JSON summaries may be produced by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI. The artifact includes a sample session summary JSON file.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
