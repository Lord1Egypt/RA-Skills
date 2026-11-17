## Description:

Generates podcast-style MP3 audio and transcripts from one or more URLs using Podcastfy with Gemini transcript generation and Edge TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[watermelon11](https://clawhub.ai/user/watermelon11)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and Clawdbot operators use this skill to convert one or more links into a conversation-style audio summary with local audio and transcript outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and executes current upstream Python packages and Playwright browser components at run time.

Mitigation: Use a dedicated isolated environment, and prefer pinned dependencies or a prebuilt environment before production use.

Risk: Runtime dependencies can access the process environment, including available credentials.

Mitigation: Run with only the needed Gemini key present and avoid providing confidential or authenticated URLs.

Risk: Generated MP3 output can be empty or truncated.

Mitigation: Validate generated MP3 duration and size, and fall back to Edge TTS synthesis from the latest transcript when needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Audio, Text, Shell commands, Configuration]

**Output Format:** [MP3 audio files, text transcripts, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and GEMINI_API_KEY; writes outputs under local audio and transcript directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
