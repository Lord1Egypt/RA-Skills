## Description: <br>
Turns meeting recordings into structured minutes with ASR transcription, speaker diarization, voiceprint-based speaker matching, LLM-generated summaries, and chunked processing for longer audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jack-Yang-ai](https://clawhub.ai/user/Jack-Yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, teams, and developers use this skill to convert recorded meetings, interviews, and internal discussions into readable minutes with participants, decisions, action items, risks, and open questions. It is best suited to offline processing where users can review speaker identities and improve accuracy with optional voiceprints or speaker maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings and transcripts may contain sensitive content that is sent to StepFun or another configured LLM endpoint. <br>
Mitigation: Use the skill only for recordings that are approved for external ASR or LLM processing, and review endpoint configuration before running it. <br>
Risk: Voiceprint enrollment and speaker identification store biometric speaker data locally. <br>
Mitigation: Obtain participant consent before enrolling or identifying speakers, and periodically delete voiceprints that are no longer needed. <br>
Risk: Local caches may retain meeting transcripts, diarization results, or other derived meeting data. <br>
Mitigation: Periodically delete ASR, diarization, and meeting-summary caches according to the user's retention policy. <br>
Risk: Speaker names that look like paths may interact poorly with current voiceprint path handling. <br>
Mitigation: Avoid names containing slashes, '..', or other path-like components until voiceprint path handling is fixed. <br>
Risk: Speaker identification may be inaccurate even when a voiceprint match is returned. <br>
Mitigation: Require a human to confirm speaker identities before treating names in the final minutes as authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jack-Yang-ai/meeting-summary) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [StepFun API key portal](https://platform.stepfun.com/interface-key) <br>
- [pyannote speaker diarization model](https://huggingface.co/pyannote/speaker-diarization-community-1) <br>
- [wespeaker speaker embedding model release](https://github.com/wenet-e2e/wespeaker/releases/download/v2.1/voxceleb_resnet34.onnx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON and Markdown meeting minutes, with shell commands and user-facing guidance during setup or execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include speaker lists, transcript segments, summaries, action items, open questions, confidence flags, and speaker-review data.] <br>

## Skill Version(s): <br>
2.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
