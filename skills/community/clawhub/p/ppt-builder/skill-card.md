## Description: <br>
Build high-quality presentation decks from scratch, covering brainstorming, content writing, visual design, AI image generation, iterative QA, and final delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to plan, write, design, generate, review, and deliver presentation decks from a topic, source material, or existing draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide prompts may be sent to external image-generation providers such as Ofox or OpenRouter. <br>
Mitigation: Do not include confidential strategy, customer data, regulated information, or unreleased product details unless the organization permits that provider use. <br>
Risk: The workflow requires sensitive API credentials for image generation. <br>
Mitigation: Use a dedicated API key with appropriate access controls and avoid sharing generated configuration files that contain secrets. <br>
Risk: Generated slide images can contain rendering errors, incorrect text, or misleading visuals. <br>
Mitigation: Review generated slides before sharing and use the QA workflow to rerun only affected pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/ppt-builder) <br>
- [Prompt Writing Guide for Nano Banana Pro](references/prompt-writing-guide.md) <br>
- [QA Fix Patterns](references/qa-fix-patterns.md) <br>
- [Spec Review Checklist](references/spec-review-checklist.md) <br>
- [Writing Principles](references/writing-principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON slide specifications, Python commands, and generated presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce content.md, design.md, slides.json, slide images, PPTX, and optional PDF artifacts through the bundled generation workflow.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
