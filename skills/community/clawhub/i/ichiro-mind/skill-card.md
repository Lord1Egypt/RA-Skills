## Description: <br>
Ichiro-Mind is a unified memory system for AI agents with HOT, WARM, COLD, and ARCHIVE layers for working state, associative recall, vector-style search, experience learning, and long-term memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hudul](https://clawhub.ai/user/hudul) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent local memory, recall, decision tracking, and MCP-accessible memory tools to AI-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist local memory and may store conversation-derived preferences, decisions, lessons, or other sensitive context. <br>
Mitigation: Use it only where persistent memory is intended, avoid entering secrets or sensitive personal data, and review local memory files and databases regularly. <br>
Risk: The security summary notes unclear consent, retention, and deletion controls for stored memories. <br>
Mitigation: Confirm storage locations, retention expectations, auto-capture behavior, and deletion procedures before enabling the skill for routine use. <br>
Risk: The skill requires an OPENAI_API_KEY for embedding or related memory functionality. <br>
Mitigation: Provide credentials through environment management, avoid committing keys, and rotate any key exposed during testing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hudul/ichiro-mind) <br>
- [Publisher profile](https://clawhub.ai/user/hudul) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Python examples, shell commands, MCP JSON configuration, and text tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory records and recall results through CLI, Python API, and MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
