## Description:

Multi Group Chat Manager helps an OpenClaw agent manage multiple chat groups by maintaining local user profiles, affection scores, session state, and rule-based OneBot message scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pppig1357](https://clawhub.ai/user/pppig1357)

### License/Terms of Use:

MIT-0

## Use Case:

Community administrators and agent builders use this skill to give an OpenClaw assistant persistent local context about group members, scan session windows, and apply configurable group-rule scoring across QQ/OneBot and other supported chat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles raw group chat messages, persistent user profiles, and reputation-style affection scores.

Mitigation: Install it only in groups where members have been clearly told that messages may be collected, analyzed, and stored for these purposes.

Risk: Weak consent and access-control boundaries could expose profile or score data to unintended users.

Mitigation: Limit operation to trusted administrators, keep profile and affection queries private, and validate user and group IDs before use.

Risk: The OneBot collector can ingest group history through an HTTP endpoint.

Mitigation: Restrict OneBot to a local trusted endpoint and avoid exposing the configured API to untrusted networks.

Risk: Persistent profiles and scores can accumulate sensitive or stale records.

Mitigation: Add retention and deletion controls before broad deployment, and review scan results before using scores for moderation decisions.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/pppig1357/skills/multi-group-chat-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local JSON profile, memory, affection-score, rule, and session-state files when the documented scripts are run.]

## Skill Version(s):

1.1.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
