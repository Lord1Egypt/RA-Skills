## Description: <br>
三國志略 / Histrategy is an AI-powered historical strategy game with Three Kingdoms and Rome Triumvirate scenarios, natural-language army commands, bilingual play, and multiplayer support through IM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a persistent, AI-assisted historical strategy game in chat or through the SDK, issuing natural-language commands for single-player or multiplayer campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gameplay history and room state can persist on local disk. <br>
Mitigation: Avoid entering sensitive information in game commands and delete saved rooms when gameplay history should not be retained. <br>
Risk: Optional LLM mode may send gameplay prompts to a configured model provider and can increase turn latency. <br>
Mitigation: Configure only approved provider API keys, use explicit commands such as /histrategy for activation, and use offline rule-based mode when external LLM calls are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergencescience/histrategy) <br>
- [Histrategy web page](https://emergence.science/en/games/histrategy) <br>
- [Histrategy SDK on PyPI](https://pypi.org/project/histrategy-sdk/) <br>
- [Histrategy project link](https://github.com/emergencescience/histrategy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [JSON responses containing Markdown-formatted game messages, help text, state summaries, and turn results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persistent room state is stored locally; optional LLM providers require API keys and offline rule-based mode is available without an API key.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
