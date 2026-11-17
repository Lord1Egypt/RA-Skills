## Description:

Control a Mopidy music system through Mopidy JSON-RPC for everyday listening, queue management, playback control, and matching ranked music requests against the local library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grantmacnamara](https://clawhub.ai/user/grantmacnamara)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search a Mopidy library, inspect playback state and queue contents, add tracks, albums, or playlists, and control playback. It also supports ranked or canonical music requests by matching externally identified songs or albums against the local Mopidy library before queueing confirmed matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some helper commands may bypass certificate checks when connecting to MOPIDY_URL.

Mitigation: Use the skill only with a trusted Mopidy server, preferably local or served over properly certificate-validated HTTPS.

Risk: The play-track and clear actions can replace or clear the current queue.

Mitigation: Confirm user intent before queue-replacing actions and prefer queue-add behavior unless the user explicitly requests immediate playback or clearing.

## Reference(s):

- [Mopidy API Notes](references/api-notes.md)
- [ClawHub skill page](https://clawhub.ai/grantmacnamara/skills/mopidy)
- [Publisher profile](https://clawhub.ai/user/grantmacnamara)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON-RPC-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, and MOPIDY_URL for helper-script workflows.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
