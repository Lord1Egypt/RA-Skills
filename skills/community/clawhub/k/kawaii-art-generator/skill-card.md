## Description:

AI kawaii art generator -- create cute kawaii characters, chibi-style illustrations, and adorable Japanese kawaii artwork with soft pastel colors, big sparkling eyes, and dreamy aesthetics via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate kawaii-style AI artwork from text prompts, with optional size selection and reference-image inheritance through a Neta API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference identifiers, and the Neta API token are sent to an external image-generation provider.

Mitigation: Use a token with limited scope or quota and avoid submitting private personal data, secrets, or confidential material.

Risk: Passing the token with the documented --token flag can expose it in shell history, process listings, or logs.

Mitigation: Avoid logging command lines that include tokens and prefer short-lived or low-quota tokens for this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/kawaii-art-generator)
- [Publisher profile](https://clawhub.ai/user/blammectrappora)
- [Neta AI token and service page](https://www.neta.art/open/)
- [Neta image generation API endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Plain text image URL printed to stdout, with progress and errors printed to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token, a text prompt, optional size selection, and an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
