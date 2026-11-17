## Description:

Generate eerie liminal space images, dreamcore backgrounds, and backrooms-style scenes via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, horror writers, social media accounts, and game or video creators use this skill to generate liminal-space, dreamcore, and backrooms-style images from text prompts. Developers can invoke it as a Node CLI with size and reference-image options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live Neta API token passed on the command line may be exposed through shell history, shared logs, or process listings.

Mitigation: Use a safer token-handling workflow, avoid elevated privileges, and avoid pasting live tokens into shared commands or logs.

Risk: Prompts and optional reference image UUIDs are sent to the Neta/Tales of AI image service.

Mitigation: Do not submit sensitive prompts or reference identifiers unless sharing them with the external image service is acceptable.

## Reference(s):

- [Neta API token signup](https://www.neta.art/open/)
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/liminal-space-generator)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
