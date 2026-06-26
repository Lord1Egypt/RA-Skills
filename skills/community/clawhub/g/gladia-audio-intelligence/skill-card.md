## Description: <br>
Helps agents configure Gladia audio intelligence features for pre-recorded and live transcription, including diarization, translation, sentiment analysis, named entity recognition, PII redaction, subtitles, summarization, chapterization, custom vocabulary, and audio-to-LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladiaio](https://clawhub.ai/user/gladiaio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Gladia audio intelligence options, combine features, and understand which capabilities are available for pre-recorded and live transcription workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio and transcripts may contain confidential, regulated, or personal data that is sent to a third-party service. <br>
Mitigation: Use the skill only for audio you are permitted to process, and check Gladia retention, security, and compliance settings before use. <br>
Risk: PII redaction can reduce downstream exposure but does not guarantee raw audio or transcript content was never processed by the service. <br>
Mitigation: Treat PII redaction as a downstream control and avoid uploading sensitive recordings unless the privacy and compliance posture is acceptable. <br>


## Reference(s): <br>
- [Live Audio Intelligence Reference](references/live-audio-intelligence.md) <br>
- [Pre-Recorded Audio Intelligence Reference](references/pre-recorded-audio-intelligence.md) <br>
- [Gladia Audio Intelligence Overview](https://docs.gladia.io/chapters/pre-recorded-stt/audio-intelligence) <br>
- [Gladia Speaker Diarization](https://docs.gladia.io/chapters/audio-intelligence/speaker-diarization) <br>
- [Gladia Translation](https://docs.gladia.io/chapters/audio-intelligence/translation) <br>
- [Gladia Sentiment Analysis](https://docs.gladia.io/chapters/audio-intelligence/sentiment-analysis) <br>
- [Gladia Named Entity Recognition](https://docs.gladia.io/chapters/audio-intelligence/named-entity-recognition) <br>
- [Gladia PII Redaction](https://docs.gladia.io/chapters/audio-intelligence/pii-redaction) <br>
- [Gladia Custom Vocabulary](https://docs.gladia.io/chapters/audio-intelligence/custom-vocabulary) <br>
- [Gladia Summarization](https://docs.gladia.io/chapters/audio-intelligence/summarization) <br>
- [Gladia Chapterization](https://docs.gladia.io/chapters/audio-intelligence/chapterization) <br>
- [Gladia Audio-to-LLM](https://docs.gladia.io/chapters/audio-intelligence/audio-to-llm) <br>
- [Gladia Live Audio Intelligence](https://docs.gladia.io/chapters/live-stt/audio-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown with TypeScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
