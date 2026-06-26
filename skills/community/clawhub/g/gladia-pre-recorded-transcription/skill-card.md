## Description: <br>
Transcribe pre-recorded audio files or URLs with Gladia for asynchronous transcription, diarization, subtitles, PII redaction, translation, named entity recognition, summarization, chapterization, and audio-to-LLM workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladiaio](https://clawhub.ai/user/gladiaio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use this skill to add Gladia pre-recorded audio and video transcription workflows, including batch jobs, polling, result retrieval, diarization, subtitles, redaction, translation, and summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio recordings may contain confidential, regulated, or third-party information before they are sent to Gladia or downstream callback and LLM destinations. <br>
Mitigation: Use the skill only when authorized to process the recordings with Gladia and any configured webhook, callback, or audio-to-LLM destination. <br>
Risk: Deleting the wrong transcription job can remove remote job data. <br>
Mitigation: Confirm job identifiers before delete operations and prefer explicit job lookup before destructive actions. <br>
Risk: Raw REST polling without backoff can waste requests and trigger rate limits. <br>
Mitigation: Prefer the official SDK polling behavior or use callbacks/webhooks; if raw REST is required, apply exponential backoff. <br>


## Reference(s): <br>
- [Delivery and Response Reference](references/delivery-and-response.md) <br>
- [Managing Pre-Recorded Jobs](references/managing-jobs.md) <br>
- [Transcription Options Reference](references/transcription-options.md) <br>
- [Pre-recorded quickstart](https://docs.gladia.io/chapters/pre-recorded-stt/quickstart) <br>
- [Audio intelligence overview](https://docs.gladia.io/chapters/pre-recorded-stt/audio-intelligence) <br>
- [API reference: pre-recorded init](https://docs.gladia.io/api-reference/v2/pre-recorded/init) <br>
- [ClawHub skill page](https://clawhub.ai/gladiaio/gladia-pre-recorded-transcription) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript and Python examples, REST endpoint references, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK-first implementation guidance, raw REST fallback steps, polling settings, callback configuration, and job-management commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
