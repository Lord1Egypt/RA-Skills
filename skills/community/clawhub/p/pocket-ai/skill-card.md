## Description:

Transcribe, index, and semantically search voice recordings while surfacing action items and meeting context for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asabovetech](https://clawhub.ai/user/asabovetech)

### License/Terms of Use:

MIT

## Use Case:

Attorneys, entrepreneurs, executives, consultants, and other Pocket AI users use this skill to let an agent search recorded conversations, retrieve meeting context, extract follow-ups, and assemble briefing material from Pocket AI data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive transcript, recording, audio, and profile-derived data through agent responses or shared channels.

Mitigation: Use it only in approved workspaces, avoid posting raw transcripts or sensitive summaries to shared channels, and review privacy, retention, regional storage, and consent requirements before use.

Risk: The skill depends on a local Pocket AI bearer token and remote Pocket AI API calls.

Mitigation: Store the token with restrictive file permissions, rotate it if exposed, and install only where remote API access to Pocket AI is acceptable.

Risk: The shell search helper interpolates user queries into JSON without robust escaping.

Mitigation: Fix JSON escaping before automation use, or prefer the Python client path that sends structured JSON through the requests library.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asabovetech/skills/pocket-ai)
- [Pocket AI API documentation](https://docs.heypocketai.com/docs/api)
- [Pocket AI product site](https://heypocket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and inline Python or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local bearer token and returns Pocket AI profile, transcript, recording, action-item, and audio-derived data from remote API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
