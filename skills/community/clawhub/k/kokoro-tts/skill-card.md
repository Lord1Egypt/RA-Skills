## Description:

Generate spoken audio from text using the local Kokoro TTS engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edkief](https://clawhub.ai/user/edkief)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to convert text into spoken MP3 audio through a configured Kokoro TTS endpoint. It is useful when an agent needs to say a message, create a voice note, or attach generated speech audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text is sent to the configured Kokoro API endpoint, which may expose sensitive content if a remote endpoint is used.

Mitigation: Use the default localhost endpoint for private text, and configure remote endpoints only when the operator trusts that server.

Risk: Generated speech output depends on the availability and behavior of the configured Kokoro API endpoint.

Mitigation: Verify the endpoint URL before use and review generated audio before sharing it externally.

## Reference(s):

- [Available Kokoro Voices](references/voices.md)
- [ClawHub skill page](https://clawhub.ai/edkief/skills/kokoro-tts)
- [Publisher profile](https://clawhub.ai/user/edkief)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Text guidance with shell commands and generated MP3 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes an MP3 file under media/ and prints a MEDIA path for agent attachment.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
