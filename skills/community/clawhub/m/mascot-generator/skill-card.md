## Description:

Generate custom brand mascots and cartoon characters with AI via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate brand mascot or cartoon character concepts from text prompts for businesses, teams, schools, gaming groups, and content channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and optional reference-image identifiers to an external image API.

Mitigation: Avoid sensitive prompts, confidential brand material, or internal asset references unless the API use has been approved for that data.

Risk: The Neta API token is passed on the command line.

Mitigation: Clear shell history after use or adapt local usage to an environment variable or secret manager before using a real account token.

Risk: Unreviewed installation sources can introduce supply-chain risk.

Mitigation: Install only from trusted sources and prefer a pinned, reviewed release.

## Reference(s):

- [Mascot Generator ClawHub page](https://clawhub.ai/blammectrappora/skills/mascot-generator)
- [Neta token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports square, portrait, landscape, and tall image sizes, plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
