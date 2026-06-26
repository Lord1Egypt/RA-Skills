## Description: <br>
MeetingClaw transcribes uploaded meeting audio with Volcengine speech recognition and generates structured Markdown meeting minutes with summaries, key points, and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaginaAa2023](https://clawhub.ai/user/MaginaAa2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to turn meeting recordings into structured minutes, summaries, key points, and follow-up tasks. It is intended for audio files that may be sent to Volcengine and the configured OpenClaw/model provider under the user's data handling policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting audio and transcript content may be sent to Volcengine and the configured OpenClaw/model provider. <br>
Mitigation: Use this skill only for recordings approved for those processors, and avoid highly confidential or regulated meetings unless policy allows the transfer. <br>
Risk: API credentials are required for Volcengine services. <br>
Mitigation: Use limited-purpose API keys and rotate or revoke them according to organizational credential policy. <br>
Risk: Cleanup behavior can remove saved meeting files from the workspace. <br>
Mitigation: Keep backups of generated minutes or adjust retention before processing recordings that must be preserved. <br>


## Reference(s): <br>
- [MeetingClaw ClawHub release page](https://clawhub.ai/MaginaAa2023/meeting-claw) <br>
- [Publisher profile](https://clawhub.ai/user/MaginaAa2023) <br>
- [Standard mode guide](references/standard_mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown meeting minutes and local workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Volcengine API credentials and a compatible OpenClaw model provider; supports common audio files and defaults to fast transcription mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
