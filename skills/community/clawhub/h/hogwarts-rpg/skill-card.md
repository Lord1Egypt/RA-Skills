## Description: <br>
Hogwarts RPG is an age-appropriate, story-driven German Hogwarts adventure where the player creates an original student character, follows the background arc of The Philosopher's Stone, and makes choices across guided scenes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siegelmaik-sketch](https://clawhub.ai/user/siegelmaik-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run an interactive, age-appropriate German role-playing story in the Hogwarts setting. The agent acts as game master, generates narrative scenes and choices, and uses bundled Python helpers for saves, relationships, scene context, world memory, and moderation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local game saves, world memory, player profile data, and moderation incident logs that may retain player-entered text. <br>
Mitigation: Avoid entering real personal details, use a trusted HOGWARTS_STATE_DIR, and periodically review or clear stored state when appropriate. <br>
Risk: Using OpenAI moderation mode can send story text to the configured moderation provider. <br>
Mitigation: Use the default OpenClaw or local moderation mode unless provider processing is acceptable, and set OPENAI_MOD_KEY only when that data flow is approved. <br>
Risk: Configurable paths or binaries can change where data is stored or which moderation command is invoked. <br>
Mitigation: Use trusted values for HOGWARTS_STATE_DIR and OPENCLAW_BIN before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/siegelmaik-sketch/hogwarts-rpg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [German narrative text with choice lists, plus inline shell commands and JSON state from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Optional environment variables configure moderation mode, moderation model/API key, and the persistent Hogwarts state directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
