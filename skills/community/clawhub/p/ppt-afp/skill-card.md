## Description:

Ppt Afp guides an agent through a workflow that collects presentation requirements, confirms a visual style, generates an outline and image prompts, creates slide images, packages a PPTX file, and sends it through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external creators, and presentation authors use this skill to turn a topic or source content into a styled slide deck with generated visuals and a PPTX deliverable. The workflow is oriented around human confirmation of presentation parameters, style choice, outline review, prompt generation, image generation, packaging, and optional Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentation files may be sent to a fixed Feishu recipient by default.

Mitigation: Make Feishu delivery opt-in for each run and require explicit recipient confirmation before sending any file.

Risk: The documented network commands disable TLS certificate verification.

Mitigation: Restore TLS verification and require trusted endpoint configuration before allowing network execution.

Risk: Runtime tools are launched through package execution commands without pinning or preinstallation from trusted sources.

Mitigation: Pin tool versions or preinstall reviewed tools from trusted sources before running the workflow.

Risk: Confidential presentation content could be exposed through image-generation services or Feishu delivery.

Mitigation: Do not use confidential content until external-service use and delivery destinations are approved for the data involved.

## Reference(s):

- [Feishu style gallery preview](https://sgl0nnj5ev.feishu.cn/docx/YV09dH7KHoKUGgxZKGVcm4MHnkf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown workflow guidance with JSON snippets, shell commands, generated image files, and PPTX file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates intermediate outline, prompt, batch JSON, image, and PPTX artifacts; Feishu sending is part of the documented workflow.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
