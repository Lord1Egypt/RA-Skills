## Description:

Guides agents to generate and edit images with GPT Image 2 through the RunComfy CLI, including endpoint selection, input schema, prompting patterns, and setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative operators, and agents use this skill to route GPT Image 2 generation or editing requests through RunComfy. It is most relevant for image outputs that need embedded text, signage, layout precision, localization, or reference-image edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and public reference-image URLs are sent to RunComfy for image generation or editing.

Mitigation: Use the skill only when RunComfy processing is intended, and avoid submitting sensitive prompts or reference images unless they are appropriate for that service.

Risk: The skill depends on a local RunComfy token and CLI installation.

Mitigation: Manage the RunComfy token carefully, prefer a pinned or local CLI install where possible, and remove credentials when they are no longer needed.

Risk: Broad image-generation requests may be routed to this skill unintentionally.

Mitigation: Use explicit GPT Image 2 wording when invoking the skill and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/gpt-image-2-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy)
- [GPT Image 2 text-to-image endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy)
- [GPT Image 2 edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files are downloaded to the requested output directory when the RunComfy CLI run succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
