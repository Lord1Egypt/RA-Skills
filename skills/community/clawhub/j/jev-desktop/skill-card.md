## Description:

Guides an agent through goal-driven or single-step desktop automation without exposing the full accessibility tree to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control desktop applications from a plain-language goal or resolve and execute one interaction at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen descriptions sent to a decision endpoint can expose private documents or form values.

Mitigation: Use only with applications and documents suitable for the configured endpoint; use --no-values for confidential screens.

Risk: High-confidence destructive desktop actions may execute without local confirmation.

Mitigation: Use --confirm-destructive whenever actions could send messages, overwrite files, delete data, confirm warnings, or affect accounts.

Risk: A changed decision endpoint can receive screen descriptions.

Mitigation: Pin and trust TYPESAFE_BASE_URL before use.

## Reference(s):

- [jev-desktop on ClawHub](https://clawhub.ai/lahfir/skills/jev-desktop)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown instructions and JSON action reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actions and stop reasons; may execute desktop interactions.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
