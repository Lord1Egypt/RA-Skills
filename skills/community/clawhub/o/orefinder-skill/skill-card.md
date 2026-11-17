## Description:

Estimate where Minecraft ores are most likely to concentrate and the best mining Y level for a given seed, version, and player position using the offline orefinder-estimate tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nazzal5448](https://clawhub.ai/user/nazzal5448)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate likely Minecraft ore concentrations, best mining Y levels, and nearby candidate areas for a seed, game version, ore, biome, and player position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run unpinned npm or PyPI orefinder-estimate packages that can change after review.

Mitigation: Use a pinned, reviewed package version and run package execution in a sandboxed environment.

Risk: Ore locations produced by the skill are statistical estimates rather than seed-exact block coordinates.

Mitigation: Present results as estimates, include uncertainty in user-facing guidance, and direct users to orefinder.io when exact seed-based locations are required.

## Reference(s):

- [Minecraft Ore Finder](https://orefinder.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are statistical estimates and should distinguish estimated mining guidance from seed-exact coordinates.]

## Skill Version(s):

0.1.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
