## Description:

Generate Infinite Pokemon map stories, terrain features, content profiles, NPC policies, and interiors from a host-supplied saved-run snapshot and output schema.

This skill is for research and development only.

## Publisher:

[shellishack](https://clawhub.ai/user/shellishack)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and players of Infinite Pokemon use this skill to let Codex continue a saved game world by proposing map stories, terrain, creatures, NPC behavior, interiors, and other structured content that fits the supplied run context and schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup workflows may clone and install dependencies from the Infinite Pokemon repository when the user asks to install or start the game.

Mitigation: Review that repository separately before running setup; during host generation jobs, use supplied local files and avoid cloning, installing dependencies, or launching another game.

Risk: Generated world content can overstate gameplay capabilities if used without the supplied schema and capability context.

Mitigation: Require the host-supplied saved-run context and output schema, and treat unsupported mechanics as planning material rather than live gameplay claims.

Risk: Installing this skill alone does not install or run Infinite Pokemon.

Mitigation: Use the complete project setup workflow for launch, and report missing private job context instead of inventing or recovering it from public source.

## Reference(s):

- [Infinite Pokemon project](https://github.com/Shellishack/infinite-pokemon)
- [Project setup README](https://github.com/Shellishack/infinite-pokemon#readme)
- [Implementation guide](https://github.com/Shellishack/infinite-pokemon/blob/main/docs/IMPLEMENTATION.md)
- [Game schemas](https://github.com/Shellishack/infinite-pokemon/tree/main/game/shared)
- [Runtime contract and capability negotiation](references/runtime-contract.md)
- [Terrain and object vocabulary](references/terrain.md)
- [Continue the land across blocks](references/continuity.md)
- [Buildings: creative exteriors, dependable services](references/buildings.md)
- [Regions spanning multiple blocks](references/regions-and-dojos.md)
- [Visual assets and image generation](references/visual-assets.md)
- [Creatures, traits, goods, and rides](references/creatures-and-economy.md)
- [Behavior contract](references/npc-behavior.md)
- [Interior design contract](references/interiors.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses with concise prose fields; Markdown guidance with inline shell commands for setup workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires host-supplied saved-run context and output schema; bundled references constrain generated content to supported game capabilities.]

## Skill Version(s):

0.2.0 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
