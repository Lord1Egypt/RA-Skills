## Description: <br>
Generates ready-to-use AI prompts from 100+ templates by selecting a template category, filling placeholders, and offering optimization guidance for writing, image generation, coding, learning, office, lifestyle, creative, and advanced prompt-engineering tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newtry](https://clawhub.ai/user/newtry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn a natural-language goal into a ready-to-use prompt for AI tools. It supports prompt creation and refinement across writing, image generation, coding, learning, office work, lifestyle planning, creative ideation, and advanced prompt-engineering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated coding prompts may lead to code, scraping steps, file operations, scheduled jobs, or third-party API instructions that are unsafe if acted on without review. <br>
Mitigation: Review generated prompts and resulting code before use, avoid including secrets, and add explicit safety constraints for scraping, file operations, schedules, and API use. <br>
Risk: Prompt output can be too broad or misaligned when the user's goal, audience, tone, constraints, or output format is underspecified. <br>
Mitigation: Ask clarifying questions and fill the template with concrete task details before finalizing the prompt. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/newtry/prompt-generator-skill) <br>
- [Complete Template Library](references/templates.md) <br>
- [Writing Templates Library](references/writing-templates.md) <br>
- [Image Templates Library](references/image-templates.md) <br>
- [Coding Templates Library](references/coding-templates.md) <br>
- [Office Templates Library](references/office-templates.md) <br>
- [Learning Templates Library](references/learning-templates.md) <br>
- [Lifestyle Templates Library](references/lifestyle-templates.md) <br>
- [Creative Templates Library](references/creative-templates.md) <br>
- [Advanced Technique Templates Library](references/advanced-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text prompt templates with optional structured sections, examples, and refinement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions before producing a prompt; outputs are drafts for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
