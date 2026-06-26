## Description: <br>
Generates scheduled TikTok draft videos for Morfeo Labs by simulating Argentine brand content and ending with an AI reveal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to guide an agent through a recurring social video production workflow for Morfeo Labs, including brand selection, image and clip generation, ffmpeg assembly, and draft-only social posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes moderation-workaround guidance. <br>
Mitigation: Remove moderation-workaround instructions and keep prompts compliant with platform and provider policies before use. <br>
Risk: The skill describes recurring automated social-content generation for brand-related videos. <br>
Mitigation: Use only authorized brand assets and social accounts, keep posts as drafts, and add human approval, stop controls, scoped credentials, and logs before drafts are posted. <br>
Risk: The skill depends on referenced runtime projects and scripts that are not included in the artifact. <br>
Mitigation: Inspect the referenced runtime project and scripts before installing or running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/morfeo-content-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, inline code blocks, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational checkpoints for image and video generation, retries, ffmpeg normalization, and draft-only posting.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
