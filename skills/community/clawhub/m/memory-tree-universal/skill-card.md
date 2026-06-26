## Description: <br>
Memory Tree 记忆树架构 — 通用版，适用于任何 AI Agent 的长期记忆系统。包含三棵树设计、热冷路径管道、14 条打分规则、数据库 Schema、检索 API 和坑点总结。当用户需要记忆系统、长期记忆、AI Agent 记忆架构时加载此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hnggoyoorle](https://clawhub.ai/user/hnggoyoorle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to design or implement a long-term memory system with source, topic, and global memory trees, scoring rules, SQLite storage, and retrieval patterns. It is intended for AI agents that need structured memory across multi-turn conversations and information compression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory design can store and reuse broad conversation content, including credential-like data. <br>
Mitigation: Use opt-in memory capture, redact secrets before storage, and avoid using it with credentials, confidential work, or regulated personal data until privacy controls are added. <br>
Risk: Stored memories may be retrieved and inserted into prompts without enough isolation or filtering. <br>
Mitigation: Add per-user or per-session isolation, retrieval filtering, retention limits, deletion controls, and review of retrieved content before prompt injection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hnggoyoorle/memory-tree-universal) <br>
- [SKILL.md](SKILL.md) <br>
- [MVP Implementation](references/mvp-implementation.py) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Quickstart](references/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, SQL, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include architecture guidance, database schemas, retrieval APIs, implementation snippets, and operational caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
