## Description:

Generate open graph social media preview images from a text prompt using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sherrihidalgolt](https://clawhub.ai/user/sherrihidalgolt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agents use this skill to request AI-generated open graph and social preview images from concise text prompts and receive a direct image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed through command-line history, logs, or copied examples.

Mitigation: Use trusted installation sources, avoid sharing commands that contain real tokens, and rotate any token that may have been exposed.

Risk: Prompts and reference image UUIDs are sent to the external Neta AI service at api.talesofai.com.

Mitigation: Do not submit confidential text or sensitive imagery unless that service's terms and retention policy are acceptable for the intended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sherrihidalgolt/skills/og-image-skill)
- [Neta AI Token Setup](https://www.neta.art/open/)
- [Neta AI Image Generation API](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text image URL printed to stdout, with shell command examples in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports square, portrait, landscape, and tall image sizes; can optionally use a reference picture UUID for style inheritance.]

## Skill Version(s):

2.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
