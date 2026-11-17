## Description:

Shared execution layer for the Ofox image API that validates low-level image generation and edit parameters, sends one synchronous request, saves returned image data to files, and reports usage token counts and computed cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this library skill to call the Ofox image API for text-to-image generation or image editing when a user explicitly requests low-level Ofox image parameters, request debugging, or plain image generation not covered by a scenario skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys can be used to make paid Ofox image API calls without a code-enforced approval step.

Mitigation: Run dry-run first, review the resolved model, count, size, and estimated cost, and proceed with a live call only after explicit user approval.

Risk: Setting OFOX_API_BASE_URL changes the host that receives OFOX_API_KEY.

Mitigation: Keep OFOX_API_BASE_URL unset unless the alternate host is intentionally trusted; require HTTPS except loopback and relay the hostname warning when an override is used.

Risk: Image editing uploads the selected local image to Ofox.

Mitigation: Confirm the selected image is intended for upload before using edit mode and avoid sending sensitive local images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/ofox-image-core)
- [Publisher profile](https://clawhub.ai/user/ofoxai)
- [Ofox image core homepage](https://github.com/ofoxai/skills/tree/main/skills/ofox-image-core)
- [Ofox app](https://app.ofox.ai)
- [Ofox image API endpoint](https://api.ofox.ai/v1/images/generations)
- [API parameter reference](artifact/references/api-params.md)
- [Pricing reference](artifact/references/pricing.md)
- [Model snapshot](artifact/references/models-snapshot.json)
- [Token anchors](artifact/references/token-anchors.json)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline bash commands and generated image file paths plus usage and cost text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and OFOX_API_KEY for live API calls; dry-run mode validates requests and estimates cost before sending a paid request.]

## Skill Version(s):

1.14.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
