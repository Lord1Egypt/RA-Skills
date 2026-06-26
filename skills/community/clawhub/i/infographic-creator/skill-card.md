## Description: <br>
Generates modern operator-style social media infographics for Twitter, LinkedIn, and Instagram using OpenAI gpt-image-2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berthelol](https://clawhub.ai/user/berthelol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, founders, marketers, and operators use this skill to plan, brand, and render structured social graphics and carousel-ready infographic concepts with reference logos, screenshots, and avatar assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenAI image calls use a sensitive API key and can incur usage charges. <br>
Mitigation: Use a project-scoped OpenAI API key with an appropriate spending limit. <br>
Risk: Selected prompts, logos, screenshots, and avatar images are sent to OpenAI for image rendering. <br>
Mitigation: Avoid confidential or internal assets unless they are approved for upload to the image service. <br>
Risk: The workflow may install Python dependencies and includes a fallback that can affect the system Python environment. <br>
Mitigation: Install dependencies in a virtual environment and avoid system-wide pip installation unless explicitly approved. <br>
Risk: Brand favicons fetched from Google may be generic, low resolution, or unsuitable for final artwork. <br>
Mitigation: Visually verify downloaded PNG assets before rendering and replace weak favicons with approved brand assets when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/berthelol/infographic-creator) <br>
- [Prompt templates](references/prompt-templates.md) <br>
- [Style guide](references/style-guide.md) <br>
- [Style tokens](references/style.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python prompt files; rendered assets are PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY and stores generated images under infographics/outputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
