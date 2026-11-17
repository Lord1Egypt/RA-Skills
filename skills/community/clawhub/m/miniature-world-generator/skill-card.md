## Description:

AI miniature world and diorama art generator - create tilt-shift miniature scenes, tiny world illustrations, hyper-detailed diorama art, and shallow-depth-of-field fantasy landscapes using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative developers use this skill to generate miniature world and diorama-style image prompts through the Neta/TalesOfAI image service. It supports text prompts, output size choices, and optional reference image identifiers for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference identifiers, and API tokens are sent to the external Neta/TalesOfAI image service.

Mitigation: Do not submit confidential prompts or reference identifiers, and use the service only when sharing that data with Neta/TalesOfAI is acceptable.

Risk: The documented token workflow can expose long-lived tokens in shell history or process arguments.

Mitigation: Prefer short-lived or scoped tokens when available, avoid pasting long-lived tokens directly into shell history, and rotate tokens if exposure is suspected.

Risk: The release has low trust-tier publisher evidence even though the security verdict is clean.

Mitigation: Install only the specific source and version you trust, and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/miniature-world-generator)
- [Neta API access](https://www.neta.art/open/)
- [TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text URL printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and sends prompts to the Neta/TalesOfAI image service.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
