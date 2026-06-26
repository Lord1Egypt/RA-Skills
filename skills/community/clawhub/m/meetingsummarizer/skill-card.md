## Description: <br>
Transcribe meetings with SenseAudio ASR speaker diarization, timestamps, and meeting-note extraction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, developers, and meeting operators use this skill to turn recorded or live meeting audio into speaker-separated transcripts, timestamps, meeting notes, decisions, and action-item candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan did not find concrete risky behavior, but its guidance says to review the skill text before installing because scanner context may be incomplete. <br>
Mitigation: Review requested credentials, file access, network access, and write actions before use, and confirm they match the expected SenseAudio transcription workflow. <br>
Risk: Meeting audio, transcripts, session identifiers, trace identifiers, and API credentials may be sensitive. <br>
Mitigation: Use SENSEAUDIO_API_KEY only as a bearer token, avoid logging secrets or provider identifiers, and treat transcript contents as sensitive output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scikkk/meetingsummarizer) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python helper code and transcript or meeting-note outputs in text, Markdown, JSON, or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce full transcripts with timestamps, meeting notes, action-item lists, speaker statistics, and optional sentiment timelines.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
