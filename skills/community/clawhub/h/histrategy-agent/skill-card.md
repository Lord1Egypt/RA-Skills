## Description:

Openclaw packages Histrategy, an AI-powered historical strategy game with Three Kingdoms and Rome Triumvirate scenarios, natural-language commands, and multiplayer IM support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

External players and community operators use this skill to run historical strategy game sessions through an OpenClaw agent, including single-player or IM-based multiplayer campaigns with natural-language turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable external histrategy packages can change behavior after installation.

Mitigation: Install in an isolated environment and pin and verify the histrategy packages before use.

Risk: Broad chat triggers and delete commands can unintentionally affect an active campaign.

Mitigation: Deploy only in intended chats, restrict trigger exposure where possible, and make destructive commands clear to operators.

Risk: The skill may use local saves and configured LLM API keys during gameplay.

Mitigation: Run with a dedicated account or environment and expose only the API keys and files required for the game.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergencescience/skills/histrategy-agent)
- [Histrategy SDK on PyPI](https://pypi.org/project/histrategy-sdk/)
- [Histrategy project website](https://emergence.science/en/games/histrategy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON response objects containing Markdown-formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Game state is stored locally under ~/.histrategy/rooms; V1 narrative play may use configured external LLM API keys.]

## Skill Version(s):

2.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
