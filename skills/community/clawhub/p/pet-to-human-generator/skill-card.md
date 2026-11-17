## Description:

Generates a realistic human portrait URL from a pet description by calling the Neta/Tales of AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate pet-to-human portrait images from text prompts and optional reference IDs for creative portraits, gifts, and social media content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference UUIDs, generation settings, and the API token are sent to the Neta/Tales of AI service.

Mitigation: Use a narrowly scoped or temporary token, avoid sensitive prompts or private reference identifiers, and avoid exposing tokens in shell history or shared logs.

Risk: The external image-generation task may be moderated, fail, time out, or return output that needs review before use.

Mitigation: Check command failures, retry or adjust prompts when needed, and review generated image URLs before publishing or using them downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/pet-to-human-generator)
- [Neta AI token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text URL printed to stdout, with command-line flags documented in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference UUID settings affect the generated image request.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
