## Description:

Generate dramatic film noir style portraits and scenes with AI via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate film noir portraits and scenes from text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user prompts, optional reference UUIDs, generated-output requests, and the Neta token to an external image API.

Mitigation: Avoid sensitive prompts or reference identifiers, use a short-lived or low-scope Neta token, and rotate any token exposed in shared shell history or logs.

Risk: Install commands can execute package code from the selected ClawHub or npx source.

Mitigation: Install from a trusted ClawHub path when possible, review or pin packages before use, and avoid running installs with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/noir-photo-generator)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [Plain text image URL with status messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and sends prompts and optional reference UUIDs to api.talesofai.com.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
