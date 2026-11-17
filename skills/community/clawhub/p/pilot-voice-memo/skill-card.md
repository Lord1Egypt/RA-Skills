## Description:

Send audio file messages between agents over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agent operators use this skill to record, send, receive, and clear audio voice memos over the Pilot Protocol network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio recordings can capture secrets, private conversations, or sensitive ambient information.

Mitigation: Record only with appropriate consent and avoid capturing sensitive content.

Risk: Voice memos may be sent to the wrong recipient if the hostname is incorrect.

Mitigation: Verify the intended recipient before running send-file commands.

Risk: Clearing received files can remove records that have not been reviewed or backed up.

Mitigation: Review or back up received files before using the clear command.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon, audio recording and playback tools, and optionally ffmpeg for audio conversion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
