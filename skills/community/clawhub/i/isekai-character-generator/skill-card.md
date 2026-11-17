## Description:

Generates isekai-inspired anime character images from text prompts through the Neta AI image generation API and returns a direct image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create isekai-inspired anime character art, original character concepts, light novel cover concepts, and character sheet images from text prompts. It supports selectable image aspect ratios and optional reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference UUIDs, and API tokens are sent to api.talesofai.com for image generation.

Mitigation: Use only with prompts and reference data acceptable to share with that service, and avoid including sensitive information.

Risk: Passing the API token through a literal --token argument can expose it through shell history or process inspection.

Mitigation: Prefer a safer token handling mechanism such as expanding a protected environment variable at invocation time, and rotate any token that may have been exposed.

Risk: The documented npx install command is unpinned and should not be run with elevated privileges.

Mitigation: Review the package before installation, avoid elevated privileges, and pin or otherwise control the installed version where operationally required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/isekai-character-generator)
- [Neta AI Access Page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; accepts a prompt, an image size option, and an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
