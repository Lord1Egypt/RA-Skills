## Description:

Transcribes local media files and supported public video links, then uses custom prompts to produce summaries, rewrites, quotes, storyboards, or translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this command-line skill to transcribe a local media file or supported public video link and turn it into summaries, meeting notes, translations, or other prompt-guided copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive recordings are uploaded for paid cloud processing, and provider retention terms may need confirmation.

Mitigation: Avoid sending sensitive recordings until the provider's retention terms and upload handling are confirmed.

Risk: Inaccurate network disclosures and filename collisions may result in the wrong video being uploaded.

Mitigation: Have the publisher correct the network disclosure and verify the selected video before processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-cross-platform-video-to-text)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain-text transcription or prompt-guided content, with command-line invocations as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one video or audio item per invocation; progress is written to standard error. Requires GUAIKEI_API_TOKEN, and cloud processing is billed by duration.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
