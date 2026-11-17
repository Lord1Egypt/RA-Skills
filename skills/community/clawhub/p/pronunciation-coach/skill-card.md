## Description:

Pronunciation coaching with real voice analysis using Azure Speech Services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazybuffon](https://clawhub.ai/user/crazybuffon)

### License/Terms of Use:

MIT

## Use Case:

External language learners and coaches use this skill to assess spoken English from audio files, review pronunciation, fluency, prosody, and phoneme-level issues, and receive focused practice guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected voice recordings and reference text to Microsoft Azure Speech Services.

Mitigation: Use it only with audio the user is comfortable sending to Azure, avoid sensitive recordings, and communicate the external processing behavior before assessment.

Risk: Azure Speech credentials and speech assessment output may be exposed on shared systems or in readable logs.

Mitigation: Use a restricted Azure Speech key, provide credentials through environment variables, rotate keys after shared-system use, and avoid running reports in terminals or CI logs visible to others.

## Reference(s):

- [Phoneme Guide](references/phoneme-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/crazybuffon/skills/pronunciation-coach)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON assessment data and human-readable text or Markdown coaching guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an audio file, reference text, Azure Speech credentials, ffmpeg, and Node.js.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
