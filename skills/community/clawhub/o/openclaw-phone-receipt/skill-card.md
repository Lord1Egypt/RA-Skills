## Description:

Trigger and manage OpenClaw outbound phone receipts via ElevenLabs and Twilio for task completion or failure notifications, including user-requested test calls and persistent receipt policy toggles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuofangzhe](https://clawhub.ai/user/tuofangzhe)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to have an agent manage phone receipt preferences and place outbound callback receipts after failures or urgent tasks. It also supports test calls, setup guidance, and fallback text summaries when phone calls are not required by policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place outbound phone calls through ElevenLabs and Twilio and may send receipt summaries through Telegram.

Mitigation: Require explicit user confirmation before any call or persistent receipt policy is enabled, and verify the destination number before use.

Risk: The skill relies on API credentials and a target phone number configured through environment variables.

Mitigation: Protect the environment file, scope the ElevenLabs API key to the minimum required access, and avoid committing credentials or personal phone numbers.

Risk: The call script sources an env file, which the security summary flags as an unsafe loading pattern.

Mitigation: Review and harden env-file sourcing before use, and source only trusted files controlled by the user.

Risk: Receipt behavior can persist across sessions through a state file.

Mitigation: Inspect the persisted phone receipt state and use `phone-receipt=off` when callback behavior should be disabled.

## Reference(s):

- [OpenClaw Phone Receipt Setup](references/setup.md)
- [Environment Example](references/env-example.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON state configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate outbound calls through ElevenLabs and Twilio, send Telegram text summaries, and persist receipt policy state when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
