## Description:

Notifies the current session user when an agent's active model changes, with heartbeat checks and cross-session pending notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wljmmx](https://clawhub.ai/user/wljmmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor model changes during agent conversations and notify the current session, including replaying a pending notification after an interrupted delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local storage may retain conversation routing or session identifiers and pending notification text longer than expected.

Mitigation: Install only where the database path is protected, define retention expectations, and periodically reset or remove stored state when it is no longer needed.

Risk: Any trusted local caller that can invoke the interrupt command can store notification text that may be replayed in a later response.

Mitigation: Limit invocation of the command to trusted integration paths and review pending notification behavior before use in shared or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wljmmx/skills/model-switch-notify)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON command results and short notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists model state, session routing metadata, heartbeat timestamps, and pending notification text in a local SQLite database.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
