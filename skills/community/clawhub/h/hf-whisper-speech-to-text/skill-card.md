## Description: <br>
Transcribe or translate audio files to text using a public Hugging Face Whisper Space over Gradio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shu-hari](https://clawhub.ai/user/shu-hari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn local audio files such as voice notes, meetings, podcasts, and interviews into transcripts, rough captions, summaries, action items, or English translations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files and filenames are sent to a public Hugging Face/Gradio transcription service. <br>
Mitigation: Use only for audio suitable for third-party processing; avoid confidential meetings, regulated data, or private recordings unless the user accepts public processing or configures a trusted private endpoint. <br>
Risk: The public free endpoint may rate limit, queue requests, or be unavailable. <br>
Mitigation: Tell the user when the backend is unavailable and offer alternatives such as a trusted private endpoint or another transcription path. <br>


## Reference(s): <br>
- [Default Hugging Face Whisper Space](https://hf-audio-whisper-large-v3-turbo.hf.space) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text transcript, optional JSON, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cleaned Chinese punctuation, raw model text, same-language transcription, or English translation depending on command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
