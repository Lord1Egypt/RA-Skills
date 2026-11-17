## Description:

Calls a remote OpenClaw instance through the OpenClaw Gateway HTTP API and preserves multi-turn sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anlinxi](https://clawhub.ai/user/anlinxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route selected prompts to a remote OpenClaw Gateway and receive its answer while reusing a session key across turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and credentials are sent to a remote OpenClaw Gateway over plaintext HTTP.

Mitigation: Install only on trusted networks and require HTTPS before using the skill with sensitive prompts or credentials.

Risk: The artifact ships a reusable bearer token.

Mitigation: Replace bundled credentials with environment-specific secrets before deployment and rotate any exposed token.

Risk: Session continuity depends on a local ~/.oc_session file.

Mitigation: Protect the session file with appropriate filesystem permissions or clear it with the provided management command when session reuse is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anlinxi/skills/oc-call)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text response or short command status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are produced by a remote OpenClaw chat completion endpoint; session continuity uses an x-openclaw-session-key value stored in ~/.oc_session.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
