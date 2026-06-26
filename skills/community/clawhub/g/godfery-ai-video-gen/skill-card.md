## Description: <br>
End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate short AI-assisted videos from text prompts, optionally add voiceover narration, and assemble image sequences or media outputs with FFmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, voiceover text, and generation inputs are sent to SkillBoss/HeyBoss services. <br>
Mitigation: Avoid confidential or regulated content unless approved for that service. <br>
Risk: The skill requires a local SKILLBOSS_API_KEY. <br>
Mitigation: Use a dedicated key and keep .env private. <br>
Risk: FFmpeg commands and output moves can overwrite selected output files. <br>
Mitigation: Review output paths before running the scripts. <br>
Risk: Generated media is downloaded and stored locally. <br>
Mitigation: Run the skill in a virtual environment or controlled workspace. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kirkraman/godfery-ai-video-gen) <br>
- [SkillBoss/HeyBoss API endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions and Python command-line workflows that produce local image, audio, and MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for external generation and FFmpeg for media assembly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
