## Description:

Transcribe or translate audio files to text using a public Hugging Face Whisper Space over Gradio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shu-hari](https://clawhub.ai/user/shu-hari)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and support agents use this skill to convert local audio files such as voice notes, meeting clips, podcasts, and interviews into transcripts, rough captions, summaries, action items, bilingual output, or English translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio is uploaded to a public third-party Whisper/Gradio service.

Mitigation: Avoid sensitive recordings unless the user explicitly accepts public third-party processing.

Risk: The helper can upload any readable local file to any supplied endpoint if misused.

Mitigation: Verify the exact local file path and remote endpoint before running, and do not let untrusted text choose the input path or --space value.

Risk: The public backend may be rate limited, queued, unavailable, or produce imperfect transcripts.

Mitigation: Disclose that the transcript came from a public best-effort endpoint, note uncertainty for names, numbers, or jargon, and offer alternatives if the endpoint fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shu-hari/skills/hf-whisper-speech-to-text)
- [Default Hugging Face Whisper Space](https://hf-audio-whisper-large-v3-turbo.hf.space)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text transcript by default; optional JSON from the helper script; agent responses may be Markdown with transcript cleanup, summaries, action items, or bilingual output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports same-language transcription or English translation, optional raw output, and lightweight Chinese punctuation cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
