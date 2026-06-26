## Description: <br>
ElevenLabs text-to-speech with mac-style say UX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffpignataro](https://clawhub.ai/user/jeffpignataro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate ElevenLabs text-to-speech responses with local playback and voice-selection guidance. It helps prepare short spoken replies, voice prompts, and sag CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent for speech generation may be processed by ElevenLabs and could expose confidential content. <br>
Mitigation: Avoid sending secrets or confidential text for speech generation and use a revocable ElevenLabs API key. <br>
Risk: Generated audio files in /tmp may contain sensitive spoken content. <br>
Mitigation: Delete generated /tmp audio files when they contain sensitive material. <br>
Risk: Use depends on the sag Homebrew formula and local sag CLI behavior. <br>
Mitigation: Install only if the sag Homebrew formula is trusted and monitor ElevenLabs API usage. <br>


## Reference(s): <br>
- [sag homepage](https://sag.sh) <br>
- [ClawHub skill page](https://clawhub.ai/jeffpignataro/miranda-sag) <br>
- [Publisher profile](https://clawhub.ai/user/jeffpignataro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and generated audio file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the sag CLI and an ElevenLabs API key; may write MP3 audio files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
