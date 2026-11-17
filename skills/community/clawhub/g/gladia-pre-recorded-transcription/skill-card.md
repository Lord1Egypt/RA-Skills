## Description:

Guides agents in transcribing pre-recorded audio or video with Gladia, including optional speaker identification, subtitles, translation, summarization, and PII redaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiaio](https://clawhub.ai/user/gladiaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users building batch transcription workflows use this skill to submit recorded media, retrieve transcripts and optional analyses, and manage asynchronous jobs through Gladia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recorded media or media URLs sent to Gladia may contain confidential, regulated, or personally identifying information.

Mitigation: Confirm the recording can be shared before submission; enable PII redaction or avoid optional analysis features when unnecessary.

Risk: Transcription callbacks can deliver job information to an untrusted endpoint.

Mitigation: Use only webhook endpoints you control and trust.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gladiaio/skills/gladia-pre-recorded-transcription)
- [Pre-recorded transcription quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart)
- [Audio intelligence overview](https://docs.gladia.io/chapters/pre-recorded-stt/audio-intelligence)
- [Pre-recorded API reference](https://docs.gladia.io/api-reference/v2/pre-recorded/init)
- [Transcription options](artifact/references/transcription-options.md)
- [Managing jobs](artifact/references/managing-jobs.md)
- [Delivery and response](artifact/references/delivery-and-response.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with JavaScript or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe transcripts, subtitles, job results, and optional audio analyses.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
