## Description: <br>
Use this skill when working with OpenRouter free LLM models, including discovering free models, selecting fallback-ranked models, proxying prompts, and scaffolding Python or TypeScript clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sh01-rgb](https://clawhub.ai/user/sh01-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route prompts through currently free OpenRouter models, compare or select model options, and generate OpenRouter client code with fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated requests may be sent to OpenRouter as an external LLM provider. <br>
Mitigation: Use the skill only for data approved for OpenRouter processing and avoid sending confidential prompts unless the environment permits it. <br>
Risk: The skill reads OpenRouter API keys from project, user, and shell environment sources. <br>
Mitigation: Use a dedicated, rotatable OpenRouter API key and avoid storing unrelated secrets in shared .env files. <br>
Risk: A user-specified or changed model may not be free at execution time. <br>
Mitigation: Confirm model choices before use and rely on the free-model discovery and fallback checks before sending requests. <br>


## Reference(s): <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter API Base](https://openrouter.ai/api/v1) <br>
- [OpenRouter Keys](https://openrouter.ai/keys) <br>
- [Model Preferences & Ranking](references/model_preferences.md) <br>
- [Python Template](references/python_template.md) <br>
- [TypeScript / JavaScript Template](references/typescript_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenRouter model IDs, fallback order, API-key setup guidance, and generated Python or TypeScript client code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
