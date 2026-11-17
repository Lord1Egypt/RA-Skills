## Description:

Helps agents edit images with OpenAI GPT Image 2 on RunComfy by producing RunComfy CLI commands, JSON inputs, and prompting guidance for targeted edits, text replacement, and multi-reference composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creative automation agents use this skill to prepare RunComfy image-edit requests for localized ad assets, brand-safe copy swaps, background changes, and multi-reference image composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and public image URLs are processed by RunComfy-hosted services.

Mitigation: Use the skill only for content acceptable for hosted processing, and avoid submitting confidential prompts or private images unless the user's RunComfy account and data handling terms allow it.

Risk: RunComfy authentication depends on a local login token or RUNCOMFY_TOKEN.

Mitigation: Use a limited token or account where possible, keep tokens out of shared logs and prompts, and prefer isolated environments for installation and execution.

Risk: Image inputs and generated outputs may contain misleading or adversarial visual content.

Mitigation: Review image URLs and generated files before reuse, especially when the output is used in brand, advertising, or user-facing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/gpt-image-edit)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-edit)
- [RunComfy GPT Image 2 edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-edit)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-edit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RunComfy CLI invocations, endpoint input schemas, prompt patterns, troubleshooting notes, and recommendations for image-editing model selection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
