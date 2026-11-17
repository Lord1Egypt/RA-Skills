## Description:

Run a Mopidy music system in party mode for group chats, letting guests search and add music while host-only approval protects playback controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grantmacnamara](https://clawhub.ai/user/grantmacnamara)

### License/Terms of Use:

MIT-0

## Use Case:

External users, party hosts, and agent developers use this skill to manage shared Mopidy music sessions where guests can contribute tracks, albums, playlists, and ranked requests without taking over playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host-level playback controls and play-now behavior can disrupt the shared queue, including clearing queued music.

Mitigation: Require host approval before playback control, queue clearing, play-now actions, or permission changes; route non-host users to guest-safe queue actions.

Risk: Several helper operations use curl -k, which weakens TLS certificate validation for the configured Mopidy endpoint.

Mitigation: Use only a trusted Mopidy endpoint and prefer a helper version that removes curl -k or otherwise enforces trusted certificate validation.

## Reference(s):

- [Mopidy Party Mode ClawHub release](https://clawhub.ai/grantmacnamara/skills/mopidy-party-mode)
- [Mopidy-Iris / Mopidy API Notes](references/api-notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell command invocations and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, and MOPIDY_URL for helper-script operation.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
