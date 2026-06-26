## Description: <br>
Oasis Audio is an AI audio narration generator that transforms your current state of mind, content you want to digest, or recent life events into personalized audio with background music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyxu](https://clawhub.ai/user/yuanyxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn requests, notes, long-form content, or recent personal context into a narrated audio piece. It is intended for personalized audio generation, content digests, learning aids, briefings, bedtime radio, and similar single-narrator listening experiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw/QClaw session history, memory notes, and USER.md to personalize audio. <br>
Mitigation: Install only when this local data access is acceptable, and use the dry-run or preview path before sending personalized prompts. <br>
Risk: Derived personal details can be sent to the xplai.ai API for audio generation. <br>
Mitigation: Review the generated prompt before transmission and require explicit confirmation before sending content that may be sensitive. <br>
Risk: Audit logging can save sent prompts locally when enabled. <br>
Mitigation: Enable audit logging only when local prompt records are intentionally needed, and avoid debug mode for private content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyxu/oasis-audio) <br>
- [Publisher profile](https://clawhub.ai/user/yuanyxu) <br>
- [xplai.ai](https://www.xplai.ai/) <br>
- [xplai.ai audio API endpoint](https://eagle-api.xplai.ai) <br>
- [Audio modes](artifact/audio_modes.md) <br>
- [Text architecture](artifact/text_architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and audio generation status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates prompts for a third-party audio API and returns an audio identifier/status for polling; generated audio is MP3 according to the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
