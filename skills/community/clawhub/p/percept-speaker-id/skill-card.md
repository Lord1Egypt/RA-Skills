## Description:

Identifies and tracks speakers in multi-person conversations, mapping speaker labels to names and managing voice-command authorization levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to attribute transcript segments to speakers, maintain a local speaker registry, and decide which speakers may trigger voice commands in Percept and Omi multi-person conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local speaker registry may contain real names, ownership or approval status, and speaker activity timestamps.

Mitigation: Confirm this data handling is acceptable before installation and restrict access to the local registry and dashboard settings.

Risk: Speaker authorization settings affect who can trigger voice commands.

Mitigation: Review who can edit Percept dashboard speaker settings and audit owner or approved status changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarvis563/skills/percept-speaker-id)
- [Percept project repository](https://github.com/GetPercept/percept)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference speaker labels, speaker profile fields, authorization states, and dashboard settings.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
