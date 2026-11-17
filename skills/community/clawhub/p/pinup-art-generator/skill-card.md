## Description:

Generate classic 1950s pin-up art, retro glamour illustrations, vintage poster portraits, mid-century advertising art, and Gil Elvgren style pinup girls via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate retro pin-up style image URLs from text prompts, with optional aspect ratio selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Neta API tokens can be exposed through shared terminals, scripts, CI logs, or shell history.

Mitigation: Pass tokens only in private execution contexts, avoid committing or logging them, and rotate any token that may have been exposed.

Risk: Prompt text and optional reference UUIDs are sent to an external image generation API.

Mitigation: Avoid sending confidential prompts or sensitive reference identifiers unless external processing is acceptable.

Risk: The artifact is published by a third-party ClawHub user rather than NVIDIA.

Mitigation: Verify the publisher profile and prefer a pinned or checksum-verified artifact before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/pinup-art-generator)
- [Neta API token signup](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL printed to stdout, with progress and errors printed to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; prompt text and optional reference UUID are sent to the external image API.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
