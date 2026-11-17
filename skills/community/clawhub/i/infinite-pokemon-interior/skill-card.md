## Description:

Design interior furniture layouts, rugs, room names, and inspectable details for new Infinite Pokemon maps within protected room and service constraints.

This skill is for research and development only.

## Publisher:

[shellishack](https://clawhub.ai/user/shellishack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game-content agents use this skill to propose inhabited interior room layouts for Infinite Pokemon maps while preserving fixed exits, protected objects, terminals, service NPCs, and schema constraints. The skill is intended for host-supplied generation jobs or setup support for the educational, non-commercial game project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path asks an agent to clone a remote repository and follow instructions that may change after this review.

Mitigation: Review the repository and README before setup, prefer a known commit or release, and run dependency installation and build steps in a least-privileged sandbox or separate project directory.

Risk: Interior proposals can be rejected or mislead users if they block protected exits, service NPCs, terminals, or claim unsupported facilities through text.

Mitigation: Keep fixed room shell elements accessible, use only supported furniture and scene IDs, and describe only services implemented by the game runtime.

## Reference(s):

- [Interior design contract](references/interiors.md)
- [ClawHub skill page](https://clawhub.ai/shellishack/skills/infinite-pokemon-interior)
- [Project repository](https://github.com/Shellishack/infinite-pokemon)
- [Skill source](https://github.com/Shellishack/infinite-pokemon/tree/main/skills/infinite-pokemon-interior)
- [Project setup](https://github.com/Shellishack/infinite-pokemon#readme)
- [Implementation guide](https://github.com/Shellishack/infinite-pokemon/blob/main/docs/IMPLEMENTATION.md)
- [Game schemas](https://github.com/Shellishack/infinite-pokemon/tree/main/game/shared)
- [Project disclaimer](https://github.com/Shellishack/infinite-pokemon/blob/main/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON room proposals for host generation jobs, or Markdown guidance with shell commands for setup support]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Room proposals must follow the host-supplied schema, use only supported scene and furniture IDs, preserve protected room elements, and avoid mutating game files.]

## Skill Version(s):

0.2.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
