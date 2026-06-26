## Description: <br>
Local video comprehension skill that uses ffmpeg to extract audio and frames, FunASR for speech recognition, and qwen3-vl for image understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomuiv](https://clawhub.ai/user/tomuiv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect videos locally by extracting speech transcripts and representative frames, then combining audio and visual observations into a summary or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary audio and frame files can contain confidential, regulated, or private video content. <br>
Mitigation: Process only videos approved for local tool handling and remove generated audio or frame files when they are no longer needed. <br>
Risk: The optional cloud LLM summary step can expose transcript or frame-derived content to a third-party provider. <br>
Mitigation: Avoid cloud summarization for sensitive videos unless the provider, data handling, and sharing implications have been explicitly approved. <br>


## Reference(s): <br>
- [Ollama download](https://ollama.com/download) <br>
- [ClawHub skill page](https://clawhub.ai/tomuiv/local-video-understanding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audio and frame files while processing video inputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
