## Description:

Jarvis TTS text-to-speech using Microsoft edge-tts with afplay playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e421083458](https://clawhub.ai/user/e421083458)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to add Chinese text-to-speech playback to an agent workflow, including voice replies, audio responses, notifications, and audiobook-style reading on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech synthesis may be sent to Microsoft's TTS service.

Mitigation: Do not use the skill to read secrets, credentials, or confidential material aloud; review whether the text is appropriate for an external TTS service before use.

Risk: The runtime depends on the pip-installed edge-tts package and macOS afplay.

Mitigation: Install dependencies in an isolated environment, pin edge-tts when reproducibility matters, and confirm the target host provides afplay before relying on playback.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, audio]

**Output Format:** [CLI text output with generated MP3 audio playback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts input text and an optional Chinese voice selection; requires macOS afplay, Python 3, edge-tts, and network access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
