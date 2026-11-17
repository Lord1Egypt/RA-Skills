## Description:

Generates neon-lit artwork from text descriptions using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate neon-styled images from text prompts via the Neta API for profile images, wallpapers, social media content, and digital art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompt, optional reference UUID, and Neta token are sent to api.talesofai.com for image generation.

Mitigation: Use a limited Neta token, run the skill only on trusted machines, and avoid submitting sensitive prompts or reference identifiers.

Risk: A floating npx install command can install code that differs from the reviewed release.

Mitigation: Prefer the ClawHub install path or another pinned, reviewed source.

## Reference(s):

- [Neta API access](https://www.neta.art/open/)
- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/neon-art-generator)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text image URL printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference UUID parameters affect the generated image.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
