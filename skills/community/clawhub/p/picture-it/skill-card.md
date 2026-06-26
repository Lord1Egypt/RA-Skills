## Description: <br>
Guides agents to generate, edit, composite, crop, and post-process images with the picture-it CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geongeorge](https://clawhub.ai/user/geongeorge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent users use this skill to plan cost-aware image creation workflows and run picture-it commands for generated images, edits, background removal, compositing, typography, and format-specific outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI image operations can upload prompts and images to fal.ai and may incur usage charges. <br>
Mitigation: Use a limited FAL key, avoid pasting secrets into chat, confirm the intended workflow before paid calls, and prefer local-only commands when privacy or cost matters. <br>
Risk: AI edits can alter product details, logos, text, or other image elements that need to remain exact. <br>
Mitigation: Use local composition or background removal workflows for accuracy-sensitive product images, and review generated files before relying on them. <br>


## Reference(s): <br>
- [Picture it! ClawHub listing](https://clawhub.ai/geongeorge/picture-it) <br>
- [Project homepage](https://github.com/geongeorge/picture-it) <br>
- [picture-it npm package](https://www.npmjs.com/package/picture-it) <br>
- [fal.ai privacy](https://fal.ai/privacy) <br>
- [Composition Guide](references/composition-guide.md) <br>
- [Prompt Library](references/prompt-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run picture-it commands that create or modify image files.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
