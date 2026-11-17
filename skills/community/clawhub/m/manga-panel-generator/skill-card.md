## Description:

Generate professional black-and-white manga panels and comic pages with dynamic poses, screentones, and authentic Japanese manga art style via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate manga-style panel imagery from text prompts, with optional panel sizing and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image identifiers are sent to the third-party Neta/Tales of AI API.

Mitigation: Avoid sending sensitive prompts or private reference IDs unless the user accepts that third-party processing.

Risk: The skill requires a Neta API token, and command-line tokens can be exposed through shell history or process inspection.

Mitigation: Use short-lived or scoped tokens where possible, avoid pasting long-lived secrets directly into commands, and rotate any token that may have been exposed.

Risk: ClawHub security guidance notes install supply-chain cautions for this third-party skill.

Mitigation: Install from a pinned or trusted release source and review the artifact before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/manga-panel-generator)
- [Neta AI Open](https://www.neta.art/open/)
- [Neta Image Generation Endpoint](https://api.talesofai.com/v3/make_image)
- [Neta Artifact Task Endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text direct image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and may take up to 90 polling attempts before returning an image URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
