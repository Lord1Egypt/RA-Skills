## Description:

Transcribe large audio files (100MB+, up to 1GB/12 hours) with speaker diarization using AssemblyAI API direct HTTP calls and no SDK dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiadong0723](https://clawhub.ai/user/jiadong0723)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to transcribe large local or URL-accessible audio recordings through AssemblyAI, returning speaker-labelled transcripts with timestamps and optional archived transcript data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files sent for transcription may contain private, regulated, or business-sensitive information.

Mitigation: Use the skill only when sending the selected audio to AssemblyAI is acceptable, and delete or protect generated transcript files when recordings contain sensitive content.

Risk: The skill asks for ASSEMBLYAI_API_KEY and the artifact text suggests sharing the key in chat.

Mitigation: Configure ASSEMBLYAI_API_KEY through a secure environment or secret mechanism and do not paste the API key into chat.

Risk: The script writes transcript JSON files locally next to the source audio.

Mitigation: Review local storage location and access controls before processing sensitive recordings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiadong0723/skills/jiadong-assembly-large-audio)
- [AssemblyAI upload API endpoint](https://api.assemblyai.com/v2/upload)
- [AssemblyAI transcript API endpoint](https://api.assemblyai.com/v2/transcript)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance]

**Output Format:** [Plain text, Markdown, JSON transcript data, and Python or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ASSEMBLYAI_API_KEY and may create local transcript JSON files alongside the source audio.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
