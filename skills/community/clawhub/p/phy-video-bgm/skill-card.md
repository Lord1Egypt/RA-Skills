## Description: <br>
Analyze a video's mood and add AI-generated BGM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to analyze a local video, generate matching background music, optionally adjust playback speed, and mix the generated audio into a final video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send video content and derived prompts to external AI services. <br>
Mitigation: Use it only with videos that are approved for Google Gemini and fal.ai processing, and manage API keys through environment variables. <br>
Risk: The workflow strips original audio and writes derived video files. <br>
Mitigation: Keep backups of source videos and review output filenames before running the mixing steps. <br>
Risk: Speed, volume, fade, style, and file path values may influence generated shell commands without explicit validation. <br>
Mitigation: Review and sanitize user-provided values before execution, especially paths and numeric filter arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-video-bgm) <br>
- [Canlah AI](https://canlah.ai) <br>
- [fal.ai Lyria2 endpoint](https://fal.run/fal-ai/lyria2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown instructions with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to create a generated WAV background track, a silent speed-adjusted video, and a final MP4 with mixed background music.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
