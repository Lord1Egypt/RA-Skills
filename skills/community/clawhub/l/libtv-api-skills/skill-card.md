## Description: <br>
通过 liblib.tv 生成 AI 图片/视频. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lg0219](https://clawhub.ai/user/lg0219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to guide LibLib.tv image and video generation workflows, including text-to-image, image-to-image, text-to-video, image-to-video, animation, status checks, and result downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses a LibLib account token and may upload prompts or image files to the LibLib.tv service. <br>
Mitigation: Review prompts and uploaded images before running generation commands, and install only if you intend to use LibLib.tv with your account. <br>
Risk: The skill directs users to install and run the external @libtv/skills npm package. <br>
Mitigation: Trust and review the external package before installation, and run commands in an environment appropriate for media generation and downloads. <br>


## Reference(s): <br>
- [LibLib.tv](https://www.liblib.tv) <br>
- [LibLib.tv API documentation](https://www.liblib.tv/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include LibLib.tv CLI commands, authentication notes, API endpoint names, task status checks, and download steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
