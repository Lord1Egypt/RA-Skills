## Description:

三國志略 / Histrategy is an AI-powered historical strategy game that supports Three Kingdoms and Rome Triumvirate scenarios, natural-language army commands, English and Chinese play, and multiplayer via IM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run chat-based historical strategy campaigns where players issue natural-language decisions and receive narrative turn results, status summaries, and advisor-style suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports runtime code from outside the packaged artifact and recommends mutable or unpinned installation paths.

Mitigation: Run it in an isolated virtual environment under a nonprivileged account, pin histrategy-sdk or the source checkout to a reviewed version or commit, and verify the imported histrategy_agent path before deployment.

Risk: Game turns and campaign state are saved locally under ~/.histrategy/rooms.

Mitigation: Deploy only where local state storage is acceptable, apply normal host file-permission controls, and avoid placing sensitive chat content in game decisions.

Risk: Broad chat triggers may activate the game during normal conversation.

Mitigation: Prefer explicit command prefixes and limit the skill to intended chats or channels.

Risk: A chat command can delete saved game state without a separate confirmation step.

Mitigation: Restrict delete-command access to trusted users or add an operator confirmation workflow before enabling shared deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergencescience/skills/histrategy)
- [Project homepage](https://github.com/emergencescience/histrategy)
- [PyPI package: histrategy-sdk](https://pypi.org/project/histrategy-sdk/)
- [Histrategy web page](https://emergence.science/en/games/histrategy)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration]

**Output Format:** [JSON response payloads containing Markdown-formatted game text, with local file-based game state managed by the runtime.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Turn results may include narrative text, faction status, advisor suggestions, and saved campaign state.]

## Skill Version(s):

2.0.0 (source: server evidence release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
