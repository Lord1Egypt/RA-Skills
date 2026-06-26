## Description: <br>
Memory Pro System helps agents store, retrieve, reason over, and evolve long-term memory using vector search, document storage, knowledge graph signals, scheduled briefings, and skill feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fluffyaicode](https://clawhub.ai/user/fluffyaicode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate a personal long-term memory service for storing notes, recalling evidence, surfacing contradictions and blind spots, generating briefings, and feeding skill feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores user content in long-term memory and daily log files. <br>
Mitigation: Do not store secrets, regulated data, confidential business notes, or sensitive personal information unless local retention, review, and deletion behavior are deliberately configured. <br>
Risk: Advanced recall, collision, distillation, and multi-hop features may process memory content with third-party LLM providers. <br>
Mitigation: Configure OpenRouter or xAI keys intentionally, review provider handling policies, and avoid sending sensitive content to LLM-backed features. <br>
Risk: Background scheduling and optional Telegram push can surface stored memory content outside the immediate command session. <br>
Mitigation: Enable scheduled tasks and Telegram only after reviewing channel configuration, notification content, and operational retention expectations. <br>
Risk: Generated or executable skills, tool calls, and webhooks can turn remembered patterns into actions. <br>
Mitigation: Review generated skills and action bindings before activation or execution, and scan the cloned repository before installing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/fluffyaicode/openclaw-memory-pro) <br>
- [Setup guide](setup.md) <br>
- [Skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include memory recall summaries, assembled evidence, skill feedback commands, operational status, and setup instructions.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
