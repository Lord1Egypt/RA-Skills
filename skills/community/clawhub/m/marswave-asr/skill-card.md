## Description: <br>
Transcribe audio files to text using local speech recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFANGO](https://clawhub.ai/user/0xFANGO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to transcribe provided audio files locally, optionally polish the transcript for readability, and export the result as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the @marswave/coli CLI and may download local speech models on first use. <br>
Mitigation: Install only if the publisher and CLI are trusted, and confirm the first-run model download is acceptable. <br>
Risk: Optional AI polishing can change punctuation, remove filler words, and improve readability rather than preserve a verbatim transcript. <br>
Mitigation: Use the no-polish option when a raw transcript is required, and request the original transcript when needed. <br>
Risk: Optional Markdown export writes a local transcript file that may contain sensitive audio content. <br>
Mitigation: Approve export only when a local transcript file is desired and handle the resulting file according to the audio's sensitivity. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xFANGO/marswave-asr) <br>
- [Publisher Profile](https://clawhub.ai/user/0xFANGO) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Conversation text with optional Markdown transcript export and JSON-parsed CLI metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detected language, emotion, audio event, duration, and an optional polished transcript.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
