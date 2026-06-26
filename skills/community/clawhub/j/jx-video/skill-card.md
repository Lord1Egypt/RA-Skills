## Description: <br>
Generate video using SkillBoss API Hub (video generation, auto-routed via /v1/pilot). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate MP4 video clips from text prompts, with optional reference images, through the SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional reference images are sent to SkillBoss for video generation. <br>
Mitigation: Only use prompts and images that are appropriate to share with SkillBoss, and avoid private media unless sharing is intended. <br>
Risk: The generated MP4 is written to the path supplied with --filename. <br>
Mitigation: Choose the output path deliberately to avoid overwriting important local files. <br>
Risk: The skill requires a sensitive SKILLBOSS_API_KEY credential. <br>
Mitigation: Provide the API key through the environment and avoid exposing it in prompts, logs, or shared command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-video) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console text and local MP4 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and uv; optional input images are encoded and sent to SkillBoss.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
