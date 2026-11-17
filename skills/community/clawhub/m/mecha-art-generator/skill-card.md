## Description:

Mecha Art Generator helps agents create anime-style mecha artwork, robot illustrations, sci-fi armor concepts, mech posters, and related concept art through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate mecha-themed image prompts, run the image-generation client, and return the resulting image URL for fanart, cosplay reference, model kit inspiration, or concept design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image prompts, optional reference UUIDs, and a Neta/TalesOfAI API token to an external image-generation service.

Mitigation: Confirm external-service use is acceptable before deployment and avoid including sensitive or confidential content in prompts or reference identifiers.

Risk: Passing real API tokens directly on the command line can expose them through shell history or process listings.

Mitigation: Prefer environment variables or a managed secret flow for tokens, and avoid pasting long-lived credentials directly into shell commands.

Risk: The documented npx install command is unpinned.

Mitigation: Prefer ClawHub installation or a pinned package/version when deploying in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/mecha-art-generator)
- [Neta AI token and API access](https://www.neta.art/open/)
- [TalesOfAI API service](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text URL with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires prompt text, a Neta API token, optional image size, and optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
