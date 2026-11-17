## Description:

Validates that each core character is shaped by the story world and that each world rule creates meaningful character dilemmas before Pilot Forge begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, story developers, and agent-assisted planning workflows use this skill after World Design and Character Arc are complete to test whether characters, world rules, dilemmas, and theme are structurally connected before moving into Pilot Forge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a sync report at CLAW_WORKSPACE/03-世界/world-character-sync.md, which may replace or conflict with an existing report.

Mitigation: Confirm the target workspace path and preserve any existing report before running the skill.

Risk: The workflow is written in Chinese and is intended for a specific story-planning sequence.

Mitigation: Confirm the project uses the expected World Design, Character Arc, Theme Lock, and Pilot Forge stages before applying its gate decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/skills/planner-world-character-sync)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Markdown report written to world-character-sync.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads world, character, and theme planning documents and produces a PASS, CONDITIONAL, or FAIL sync report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
