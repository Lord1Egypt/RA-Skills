## Description: <br>
PPT AFP automates presentation creation from a user-provided topic or content by guiding style selection, outline generation, prompt creation, AI image generation, PPTX packaging, and optional Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and presentation creators use this skill to turn topics, outlines, or source documents into slide decks with selected visual styles, generated slide prompts, AI-produced slide images, and a packaged PPTX file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content may be processed by external image-generation services and can be sent through Feishu. <br>
Mitigation: Use only content approved for those services, make Feishu delivery explicit opt-in, and confirm the recipient before upload or sending. <br>
Risk: The artifact uses TLS-disabling environment settings for networked commands. <br>
Mitigation: Remove the TLS-disabling environment variable and use validated HTTPS endpoints before running generation or packaging commands. <br>
Risk: The workflow relies on local helper scripts from other skills. <br>
Mitigation: Verify the referenced helper scripts and their dependencies before running the workflow in a production or sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yipng05-max/ppt-afp) <br>
- [Feishu style gallery document](https://sgl0nnj5ev.feishu.cn/docx/YV09dH7KHoKUGgxZKGVcm4MHnkf) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON batch configuration, generated prompt files, slide images, and PPTX output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use external image-generation services and optional Feishu file delivery.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
