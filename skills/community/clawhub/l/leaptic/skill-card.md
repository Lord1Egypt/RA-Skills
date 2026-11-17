## Description:

Leaptic captures every movement and highlight in front of the lens, making every moment shine instantly, and this OpenClaw skill supports Leaptic device snapshot and status access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leaptic-tech](https://clawhub.ai/user/leaptic-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure authenticated Leaptic device snapshot access and retrieve read-only device status such as battery, charging state, storage, media counts, and latest capture time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Leaptic App-Key can expose read-only device snapshot metadata if mishandled.

Mitigation: Use platform secret injection, an OS secret store, or a session-only environment variable; if a plaintext credentials file is used, restrict its permissions.

Risk: Sending the App-Key to an untrusted endpoint could disclose credentials.

Mitigation: Use only the official regional HTTPS endpoint or a custom endpoint the user explicitly trusts, and ask for the region when the base URL is missing.

Risk: Device snapshots can include serial numbers, battery state, storage details, media counts, and timestamps.

Mitigation: Treat snapshot responses as device metadata, avoid unnecessary logging or sharing, and surface only the fields needed for the user's task.

## Reference(s):

- [Leaptic Homepage](https://www.leaptic.tech/)
- [ClawHub Leaptic Skill Page](https://clawhub.ai/leaptic-tech/skills/leaptic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to request missing App-Key or region information before API use and to interpret Leaptic device snapshot JSON responses.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
