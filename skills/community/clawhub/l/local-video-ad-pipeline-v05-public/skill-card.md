## Description: <br>
Local Video Ad Pipeline v0.5 helps agents produce short commercial videos and YouTube Shorts with local AI models for planning, keyframes, sequential Wan2.2 animation, optional BGM, subtitle timing, QA contact sheets, and final MP4 assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k0103292xxxx](https://clawhub.ai/user/k0103292xxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and video-production engineers use this skill to coordinate a local GPU workflow for generating short advertising videos, including pre-production JSON, image keyframes, animated shots, subtitles, optional background music, and final video assembly. It is intended for local model stacks where image, video, and music services must be run sequentially. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill can load Python code from user-supplied paths. <br>
Mitigation: Review the local scripts before use and supply only trusted Qwen GUI directories and module names. <br>
Risk: The security summary says generated videos can be sent through Telegram with a configured bot token. <br>
Mitigation: Avoid the Telegram delivery fallback unless upload through Telegram is explicitly desired, and never expose the configured token in chat logs or project files. <br>
Risk: The security guidance calls for neutral casting, conservative styling, subtitle-language, and cleanup expectations before running the pipeline. <br>
Mitigation: Specify casting, age-safety, styling, subtitle language, retention, and cleanup requirements before generation begins. <br>
Risk: The artifact workflow runs local GPU services and assumes sequential use of model stacks. <br>
Mitigation: Run only trusted local ComfyUI, Wan2.2, and ACE-Step services, and operate one model server class at a time as the artifact guidance describes. <br>


## Reference(s): <br>
- [ACE-Step BGM](references/ace_bgm.md) <br>
- [Character Consistency Workflow](references/character_consistency.md) <br>
- [Expression Language](references/expression_language.md) <br>
- [Pre-production Scripting](references/preproduction.md) <br>
- [Subtitle-Based Variable Timing](references/subtitle_timing.md) <br>
- [Wan2.2 Server Tuning](references/wan22_server.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON schemas, file paths, and local pipeline instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When followed by an agent with the required local services, the workflow can produce project JSON files, keyframes, video clips, subtitles, optional audio, QA contact sheets, and a final MP4.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
