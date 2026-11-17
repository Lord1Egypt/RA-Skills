## Description: <br>
记忆编排器 helps AI agents manage durable memory through four memory tiers, hybrid retrieval, summarization, persistence, health checks, and conflict handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add memory orchestration to long-running assistants, chatbots, RAG systems, and multi-agent workflows that need searchable, persistent, and reviewable context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation memory to disk, including personal preferences or other sensitive context. <br>
Mitigation: Choose an explicit storage path, avoid storing secrets or highly sensitive personal data, and review retention and deletion settings before enabling persistence. <br>
Risk: Cleanup logs and durable memory files may expose remembered user context. <br>
Mitigation: Treat memory stores and cleanup logs as sensitive files and review them before sharing, committing, or moving them to another system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-orchestrator-v2) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and TypeScript-style examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to persist memory files, emit cleanup logs, and configure optional vector-database-backed semantic retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
