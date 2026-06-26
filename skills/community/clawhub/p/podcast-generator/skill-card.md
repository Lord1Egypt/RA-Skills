## Description: <br>
Converts articles, blog posts, or other text into podcast scripts and optional TTS audio, with solo or dialogue episode formats and SkillPay billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elevo11](https://clawhub.ai/user/elevo11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, content creators, and developers use this skill to turn source text into podcast scripts, generate audio files when TTS tooling is available, and track generation statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid SkillPay charges. <br>
Mitigation: Require explicit user confirmation before each charge and review real-credential use before installing. <br>
Risk: User text may be processed through external billing or TTS tooling. <br>
Mitigation: Avoid sensitive or proprietary text unless users accept the external data flow. <br>
Risk: Generated files and local statistics can expose episode titles or overwrite chosen output paths. <br>
Mitigation: Use non-sensitive output paths, review filenames before running, and clear the local stats file when episode titles are private. <br>


## Reference(s): <br>
- [Podcast Generator ClawHub page](https://clawhub.ai/elevo11/podcast-generator) <br>
- [Script Templates](references/script-templates.md) <br>
- [SkillPay API endpoint](https://skillpay.me/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Audio files, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown podcast scripts, MP3 audio files when edge-tts is installed, and JSON or status text for billing and statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY for billing; edge-tts and ffmpeg improve audio generation; local statistics retain recent generation metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
