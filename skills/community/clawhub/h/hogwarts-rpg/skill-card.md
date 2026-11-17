## Description:

Hogwarts RPG is a German-language, age-appropriate story-game skill that guides an agent through a persistent seven-year Hogwarts role-playing adventure with character creation, choice handling, moderated scenes, and saved world memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siegelmaik-sketch](https://clawhub.ai/user/siegelmaik-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to run a German, age-appropriate interactive Hogwarts RPG where the player creates a protagonist, makes story choices, and continues across saved sessions. Agents use the bundled Python helpers to retrieve scene context, advance choices, enforce moderation checks, manage saves, and recall player-created world facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moderation and helper-command execution can expose risk when untrusted text is passed through command workflows.

Mitigation: Review command construction before installation, run the skill in a restricted environment, and avoid shell-interpolating player or model text.

Risk: Persistent saves, incident logs, and world memory may store user-provided or model-generated content outside the skill directory.

Mitigation: Treat persistent state as untrusted data, place HOGWARTS_STATE_DIR in a controlled location, and use the provided list, remove, and clear flows for memory review.

Risk: Save identifiers and state paths need containment to avoid unintended file access.

Mitigation: Validate save IDs before use and confine runtime state to a dedicated directory with least-privilege filesystem permissions.

Risk: The role-control language and seven-year story scope require review before child-facing use.

Mitigation: Confirm the full content scope, moderation behavior, and age-appropriateness before deployment, especially for externally accessible sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siegelmaik-sketch/skills/hogwarts-rpg)
- [Publisher profile](https://clawhub.ai/user/siegelmaik-sketch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration, Guidance]

**Output Format:** [German narrative text and choice prompts, with inline shell commands and JSON/status output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Player-facing scenes are intended to be concise per turn; state, memories, moderation incidents, and scene data may persist outside the skill directory.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
