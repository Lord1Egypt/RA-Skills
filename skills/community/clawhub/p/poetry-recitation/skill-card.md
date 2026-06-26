## Description: <br>
Generates poetry recitation videos with synthesized or cloned voice narration, a starry background, and timed Chinese subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn poems or short literary text into narrated MP4 recitation videos with voice audio and timed Chinese subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use locally available cloned voices, which may raise voice identity, consent, or impersonation concerns. <br>
Mitigation: Use only voices you are authorized to use, and review the selected voice, poem text, and generated output before sharing the video. <br>
Risk: The skill depends on a local TTS pipeline and writes generated audio/video files to the local workspace. <br>
Mitigation: Run it in a trusted agent environment, verify the local TTS setup before use, and confirm the output path when handling sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyanbo2007/poetry-recitation) <br>
- [Publisher profile](https://clawhub.ai/user/zhangyanbo2007) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [MP4 video file with console status text and agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1920x1080 H.264/AAC video files, typically saved under the local audio workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
