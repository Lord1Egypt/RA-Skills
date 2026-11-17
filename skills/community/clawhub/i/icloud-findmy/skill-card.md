## Description:

Query Find My locations and battery status for family devices via iCloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liamnichols](https://clawhub.ai/user/liamnichols)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use this skill to query iCloud Find My through the PyiCloud icloud CLI for device locations, battery levels, charging status, and proactive battery warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose highly sensitive Find My location and family device data.

Mitigation: Use it only for devices and family members who have consented, and avoid proactive tracking unless the user explicitly requests it.

Risk: Apple ID details and iCloud session data may be stored locally.

Mitigation: Do not store the Apple ID in ordinary workspace files, and keep local session files protected by the user's operating system account controls.

Risk: The artifact includes an unsafe eval-based parsing example for location output.

Mitigation: Replace eval with a safe parser such as JSON parsing or ast.literal_eval with validation before using parsed location data.

Risk: Automated installation depends on the external PyiCloud package.

Mitigation: Pin and review the PyiCloud version before automated installation.

## Reference(s):

- [PyiCloud](https://github.com/picklepete/pyicloud)
- [ClawHub iCloud Find My Skill](https://clawhub.ai/liamnichols/skills/icloud-findmy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and parsing examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, the PyiCloud icloud CLI, Apple ID authentication, and user consent for device or family location access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
