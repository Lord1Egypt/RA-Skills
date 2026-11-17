## Description:

Local video comprehension skill that uses ffmpeg to extract audio and frames, FunASR for speech recognition, and qwen3-vl for image understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide local video analysis workflows that extract audio, sample frames, transcribe Chinese speech with FunASR, inspect frames with qwen3-vl via Ollama, and optionally combine results into a summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cloud LLM summarization may send video-derived transcripts or frame descriptions off-device.

Mitigation: Use local-only processing unless a cloud provider is explicitly selected and the user is comfortable sending that content.

Risk: Video files may contain private, confidential, or regulated content.

Mitigation: Review content sensitivity before installation or use, and avoid cloud summarization for protected content.

Risk: The workflow depends on local tools, models, and packages installed outside the skill artifact.

Mitigation: Install dependencies in an isolated environment and prefer pinned or verified packages and models.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomuiv/skills/local-video-understanding)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command snippets and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, transcript excerpts, frame descriptions, and optional summary guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
