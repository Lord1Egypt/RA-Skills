## Description:

Mud Adventure is a Chinese-language skill that helps agents create runnable Python text-adventure and MUD games with world design, maps, NPCs, items, quests, dialogue trees, and example code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weistiger](https://clawhub.ai/user/weistiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, game designers, writers, and external users use this skill to have an agent draft Chinese-language MUD/text-adventure worlds and assemble runnable single-file Python game templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples that adopt save/load behavior may create or overwrite a local savegame.json file in the game directory.

Mitigation: Review generated file paths before running the game and keep save files scoped to the intended project directory.

Risk: The documentation and generated examples are Chinese-first, which may cause usability or review issues for non-Chinese-language users.

Mitigation: Review user-facing text and translate or localize generated game content before sharing it with the intended audience.

## Reference(s):

- [World Design Guide](artifact/references/world-design.md)
- [Game Systems Design Guide](artifact/references/game-systems.md)
- [Example Code Snippets](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first content; generated game examples may include local save-game persistence when save/load patterns are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
