## Description: <br>
三國志略 / Histrategy - AI-powered historical strategy game. Supports Three Kingdoms and Rome Triumvirate scenarios. Command armies through natural language. Multiplayer via IM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and game hosts use this skill to run turn-based historical strategy campaigns through natural-language commands in single-player or shared chat sessions. It supports Three Kingdoms and Rome Triumvirate scenarios with English and Chinese gameplay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign history is saved locally and may include player decisions or chat context. <br>
Mitigation: Use the skill only where local saved game history is acceptable, and review or delete saved rooms when campaign data should not persist. <br>
Risk: When an LLM provider is configured, turn text may be sent to that provider for narrative generation. <br>
Mitigation: Configure only approved LLM providers and API keys for the expected chat content, or use the offline rule-based mode when external transmission is unsuitable. <br>
Risk: In shared chats, the visible delete command may remove a shared saved campaign without a confirmation step. <br>
Mitigation: Enable shared play only in trusted chats and make deletion expectations clear before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergencescience/histrategy-agent) <br>
- [histrategy-sdk on PyPI](https://pypi.org/project/histrategy-sdk/) <br>
- [Histrategy website](https://emergence.science/en/games/histrategy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON response containing Markdown-formatted game text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bilingual game narratives, state summaries, help text, and command results.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
