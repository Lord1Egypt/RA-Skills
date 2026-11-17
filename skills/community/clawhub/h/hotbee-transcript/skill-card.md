## Description:

Use when a user wants audio or video converted to text through HotBee speechToText, including file URL transcription, video URL transcription, or transcript extraction from parsed social videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanye1402-hash](https://clawhub.ai/user/shanye1402-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to convert audio or video URLs into text transcripts through HotBee speechToText.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to execute mutable GitHub-hosted CLI code with an API key.

Mitigation: Review before installing and prefer an immutable reviewed package or commit before production use.

Risk: The CLI transport sends API keys and media URLs as query parameters.

Mitigation: Use only media the user is allowed to submit, prefer non-sensitive or short-lived media URLs, and avoid logging keys or signed/private URL parameters.

Risk: Live calls may consume HotBee quota and send media URLs to an external service.

Mitigation: Confirm user intent before live calls unless already approved and scope environment secrets to only HOTBEE_API_KEY.

## Reference(s):

- [Speech To Text API](references/api.md)
- [HotBee Skills](https://www.hotbee.cn/skills)
- [ClawHub skill page](https://clawhub.ai/shanye1402-hash/skills/hotbee-transcript)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and transcript text returned from the HotBee CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HOTBEE_API_KEY and a file_url or video_url for live transcription.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
