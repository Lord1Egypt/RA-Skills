## Description:

Generate grounded NPC intentions, dialogue, memory and optional movement policies for Infinite Pokemon from a supplied saved-run observation or map-design context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shellishack](https://clawhub.ai/user/shellishack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game authors use this skill to generate NPC intentions, dialogue, memory, and optional movement policies for Infinite Pokemon from host-supplied saved-run or map-design context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional setup path can clone and run an unpinned external game repository.

Mitigation: Review the upstream repository and README, prefer a known commit or release, and run dependency installation and build steps in an isolated environment without unnecessary credentials or sensitive files.

Risk: NPC generation depends on host-supplied saved-run or map-design context.

Mitigation: Use only the supplied game context for live jobs and report missing job-specific context instead of inferring private save history from source links.

Risk: Generated dialogue, memory, or movement proposals can overstate game effects if they exceed the behavior contract.

Mitigation: Keep memories grounded in observed events, keep service NPCs stationary when needed, and leave movement, collision, healing, rewards, and progression enforcement to the game engine.

## Reference(s):

- [Behavior contract](references/behavior.md)
- [ClawHub skill page](https://clawhub.ai/shellishack/skills/infinite-pokemon-npc)
- [Project repository](https://github.com/Shellishack/infinite-pokemon)
- [Skill source](https://github.com/Shellishack/infinite-pokemon/tree/main/skills/infinite-pokemon-npc)
- [Project setup](https://github.com/Shellishack/infinite-pokemon#readme)
- [Implementation guide](https://github.com/Shellishack/infinite-pokemon/blob/main/docs/IMPLEMENTATION.md)
- [Game schemas](https://github.com/Shellishack/infinite-pokemon/tree/main/game/shared)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses with concise text guidance and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live NPC jobs require host-supplied context and output schema; setup guidance may reference the complete upstream game checkout.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
