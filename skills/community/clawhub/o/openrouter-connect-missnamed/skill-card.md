## Description:

Helps agents discover currently free OpenRouter models, select a ranked fallback model, proxy prompts through OpenRouter, and scaffold Python or TypeScript clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sh01-rgb](https://clawhub.ai/user/sh01-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route prompts through currently free OpenRouter LLMs, compare model availability, and generate reusable Python or TypeScript client code with fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project, global, and process environment sources to find an OpenRouter API key.

Mitigation: Prefer exporting only OPENROUTER_API_KEY for the agent process and avoid storing unrelated secrets in ~/.env.

Risk: Prompts are sent to OpenRouter for model responses.

Mitigation: Avoid sending sensitive prompts or confidential data unless OpenRouter use is approved for that data.

Risk: The skill writes a shared model cache under /tmp.

Mitigation: Harden, isolate, or disable the shared /tmp cache when using the skill around sensitive workflows.

## Reference(s):

- [OpenRouter model API](https://openrouter.ai/api/v1/models)
- [OpenRouter API base](https://openrouter.ai/api/v1)
- [OpenRouter keys](https://openrouter.ai/keys)
- [Model Preferences & Ranking](references/model_preferences.md)
- [Python Template](references/python_template.md)
- [TypeScript / JavaScript Template](references/typescript_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, optional JSON responses, and generated Python or TypeScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream model responses and may write a local free-model cache.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
