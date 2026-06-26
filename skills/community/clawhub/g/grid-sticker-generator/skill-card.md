## Description: <br>
A universal 4x4 grid sticker generator. uses strict visual guidelines (No Text, Transparent BG) and supports loading theme templates from resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanyang](https://clawhub.ai/user/guanyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent in building prompts for 4x4 transparent-background sticker sheets from a character, theme, or office-worker template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default office-worker template may be applied when the user does not specify another theme. <br>
Mitigation: Specify the desired theme or custom action list when invoking the skill. <br>
Risk: Uploaded personal photos may expose visible appearance traits to the image generation workflow. <br>
Mitigation: Avoid uploading sensitive personal photos unless that use is appropriate for the deployment context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guanyang/grid-sticker-generator) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [office_worker_template.md](artifact/resources/office_worker_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Image generation prompts] <br>
**Output Format:** [Markdown guidance with structured image-generation prompt details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to use an available image generation tool; the skill itself declares no required credentials or shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
