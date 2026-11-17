## Description:

Generates Renaissance-style oil painting portraits of pets from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create royal Renaissance-style pet portraits for custom art, social content, gifts, and wall art from pet descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Neta API token is a secret and could be exposed if entered into shared terminals, scripts, or logs.

Mitigation: Use local secret handling where possible and avoid committing, logging, or sharing literal token values.

Risk: Prompts and optional reference image UUIDs are sent to an external image-generation API.

Mitigation: Do not submit confidential, regulated, or sensitive personal information unless the external API terms and data handling are acceptable.

Risk: Mutable install commands can install a version that differs from the reviewed artifact.

Mitigation: Prefer pinned versions or ClawHub-managed installation sources when deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/pet-renaissance-portrait-generator)
- [Neta API access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with optional Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; accepts a text prompt, output size, and optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
