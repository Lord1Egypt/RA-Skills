## Description: <br>
Ultimate AI agent memory system for Cursor, Claude, ChatGPT and Copilot, combining WAL protocol, vector search, git-notes, local archives, and optional cloud backup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add durable working memory, semantic recall, decision logging, and human-readable memory archives across agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can silently retain sensitive conversation content, preferences, decisions, and embeddings beyond the current session. <br>
Mitigation: Install only when durable memory is intended; avoid secrets and regulated data, review local memory files and vector stores regularly, and delete stale or sensitive entries. <br>
Risk: Optional SkillBoss cloud backup and auto-extraction can send conversation content and stored memories to a third-party service using an API key. <br>
Mitigation: Enable cloud backup and auto-extraction only after confirming the data boundary; use a revocable API key and confirm how to disable or delete cloud memories. <br>
Risk: Automatically injected or stale memories can influence future agent behavior with outdated or incorrect context. <br>
Mitigation: Keep auto-capture thresholds conservative, periodically audit recalled memories, and curate MEMORY.md and daily logs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-elite-longterm-memory) <br>
- [npm package](https://www.npmjs.com/package/elite-longterm-memory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local memory files and directories through the included CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
