## Description: <br>
Apply Protoss-style (StarCraft) psionic effects to any audio file as a post-processing layer for TTS or user recordings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vemec](https://clawhub.ai/user/vemec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transform existing TTS output or user recordings into processed Protoss-style voice effects with local SoX and FFmpeg commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local ffmpeg and sox commands on selected audio files. <br>
Mitigation: Use it only on audio files the user intends to process, and review the selected input path before execution. <br>
Risk: The script writes a processed file next to the input and removes temporary intermediate files. <br>
Mitigation: Keep backups or ask the agent to preserve raw or intermediate recordings when those files matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vemec/protoss-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Audio file with a _psionic suffix, with optional Markdown shell commands or delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and sox binaries; temporary intermediate audio files are cleaned up by the script.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
