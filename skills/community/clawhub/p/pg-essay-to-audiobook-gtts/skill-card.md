## Description:

Google Text-to-Speech (gTTS) converts text into audio for audiobooks, podcasts, and speech synthesis, including long text handled by sentence-boundary chunking and pydub concatenation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to add text-to-speech workflows to agents, including examples for generating MP3 files, handling long documents, and concatenating audio segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text processed by gTTS is sent over the network to Google's service.

Mitigation: Avoid submitting confidential or restricted text unless the use is approved for that external service.

Risk: The workflow depends on runtime packages and network availability for text-to-speech generation.

Mitigation: Install dependencies in a virtual environment, consider pinning reviewed package versions, and handle network failures gracefully.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides implementation patterns for generating MP3 audio; audio files are produced only when the user executes the supplied code or commands.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
