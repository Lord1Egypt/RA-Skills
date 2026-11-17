## Description:

Leaptic provides agent guidance for reading Leaptic device snapshot and status data through the documented HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulei2140](https://clawhub.ai/user/liulei2140)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure Leaptic credentials and retrieve device snapshot information such as battery, charging state, storage, media counts, and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The App-Key can access Leaptic device snapshot information.

Mitigation: Prefer environment injection or an OS secret store; keep any plaintext credentials file permission-restricted.

Risk: Sending the App-Key to an untrusted endpoint could expose device access credentials.

Mitigation: Use only official Leaptic regional endpoints or a deployment URL the user explicitly trusts.

Risk: Blind retries across different domains after failures could leak credentials.

Mitigation: Do not retry the same key on another domain; surface the error and ask the user to verify or rotate the key.

## Reference(s):

- [Leaptic homepage](https://www.leaptic.tech/)
- [ClawHub skill page](https://clawhub.ai/liulei2140/skills/lp-test)
- [Publisher profile](https://clawhub.ai/user/liulei2140)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides credential setup and API request handling; does not produce device data without user-provided credentials.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
