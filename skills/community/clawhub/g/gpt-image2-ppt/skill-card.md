## Description: <br>
Generates 16:9 presentation decks from Markdown or JSON outlines using OpenAI gpt-image-2, with curated visual styles, template-clone mode, an HTML viewer, and PPTX output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juneyaooo](https://clawhub.ai/user/juneyaooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business users use this skill through an agent to turn an outline or reference deck into presentation assets: generated slide images, a keyboard-navigable HTML viewer, and a PPTX deck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide outlines, templates, and generated prompts may be sent to remote AI endpoints. <br>
Mitigation: Avoid confidential decks unless the endpoint and credential handling are approved for that content. <br>
Risk: The skill requires sensitive credentials for direct API use. <br>
Mitigation: Store API keys only in the documented scoped environment file or an explicitly chosen credentials path, and review permissions before installation. <br>
Risk: Optional workflows can run local conversion tools, Docker, LibreOffice, or broad agent execution through a Codex backend. <br>
Mitigation: Use a controlled workspace, review templates before conversion, and disable or avoid the Codex backend when broad automated execution is not acceptable. <br>


## Reference(s): <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [English User Documentation](artifact/docs/README.en.md) <br>
- [Installation Guide](artifact/docs/install.md) <br>
- [OpenAI Images API Documentation](https://platform.openai.com/docs/guides/images) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance plus generated PNG images, an HTML viewer, JSON prompt records, and a 16:9 PPTX file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use sensitive API credentials, remote image or vision endpoints, and local presentation conversion tools depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
