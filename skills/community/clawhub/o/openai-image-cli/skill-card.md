## Description: <br>
Generate, edit, and manage images via OpenAI's GPT Image and DALL-E models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to guide agents in installing, authenticating, and operating the OpenAI Image CLI for image generation, editing, variation, batch processing, configuration, model listing, and local history management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenAI API keys may be exposed if copied into shell history, local config, logs, or shared prompts. <br>
Mitigation: Prefer environment variables or secure secret storage, avoid sharing credentials, and clear local history after sensitive work. <br>
Risk: Image prompts, source images, and generated outputs can contain sensitive or regulated information. <br>
Mitigation: Submit sensitive images or prompts only when approved for the intended environment and data handling policy. <br>
Risk: The skill depends on a third-party npm package and local CLI behavior outside NVIDIA control. <br>
Mitigation: Install only if the publisher and package are trusted, and review package updates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G9Pedro/openai-image-cli) <br>
- [npm package: @versatly/openai-image-cli](https://www.npmjs.com/package/@versatly/openai-image-cli) <br>
- [GitHub repository: Versatly/openai-image-cli](https://github.com/Versatly/openai-image-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI may save image files locally, return JSON when requested, and maintain local generation history.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
