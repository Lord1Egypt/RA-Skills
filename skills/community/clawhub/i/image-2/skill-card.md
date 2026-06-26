## Description: <br>
GPT-4o Image Generation & Editing Skill - Create, edit, transform, and analyze images using GPT-4o native image-2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gpt](https://clawhub.ai/user/gpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to create, edit, vary, and analyze images for marketing visuals, product photography, illustrations, UI mockups, and related visual content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected local images or image URLs may be sent to OpenAI for generation, editing, variation, or analysis. <br>
Mitigation: Use only approved content and avoid confidential, personal, regulated, or proprietary images unless the deployment has approved OpenAI processing for that data. <br>
Risk: The artifact under-discloses off-device image processing and incorrectly suggests images are not kept off-device. <br>
Mitigation: Review the security summary with users before installation and ensure deployment documentation accurately describes OpenAI processing and applicable retention terms. <br>
Risk: Generated and edited images are saved locally by default and may contain sensitive visual content. <br>
Mitigation: Choose approved output directories, review generated files before sharing, and remove outputs that should not remain in the workspace. <br>


## Reference(s): <br>
- [ClawHub Image-2 listing](https://clawhub.ai/gpt/image-2) <br>
- [README.md](README.md) <br>
- [Prompt gallery](examples/prompts-gallery.md) <br>
- [Quick start templates](examples/quick-starts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance, JavaScript API call patterns, JSON-like result objects, and locally saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENAI_API_KEY and saves generated or edited images locally by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
