## Description: <br>
Gipformer ASR transcribes Vietnamese audio using the g-group-ai-lab/gipformer-65M-rnnt model with server-side VAD chunking, batching, and WAV, FLAC, OGG, MP3, and M4A support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-ggroup](https://clawhub.ai/user/ai-ggroup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to transcribe Vietnamese speech from local audio files or through a local HTTP service, receiving full transcripts with chunk timing metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio recordings and transcripts may contain private or sensitive information. <br>
Mitigation: Run the server locally for private use, keep it bound to 127.0.0.1, and avoid sending audio to remote servers unless that environment is trusted and secured. <br>
Risk: Model and dependency supply chain trust affects transcription privacy and reliability. <br>
Mitigation: Install in a virtual environment and review the Python dependencies and Hugging Face model source before deployment. <br>
Risk: Binding the service to 0.0.0.0 or using a remote server can expose audio submissions and transcripts beyond the local machine. <br>
Mitigation: Use non-local binding only in a secured environment with appropriate access controls and transport protections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-ggroup/gipformer) <br>
- [Gipformer ASR Server API Reference](references/api.md) <br>
- [g-group-ai-lab/gipformer-65M-rnnt model](https://huggingface.co/g-group-ai-lab/gipformer-65M-rnnt) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcripts or JSON objects with transcript, duration, processing time, and per-chunk timing fields; guidance may include Markdown with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include per-chunk start and end timestamps. M4A support requires ffmpeg, and the server downloads ASR and VAD models on first run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
