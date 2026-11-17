## Description:

Memory Tree 记忆树架构 — 通用版，适用于任何 AI Agent 的长期记忆系统，包含三棵树设计、热冷路径管道、14 条打分规则、数据库 Schema、检索 API 和坑点总结。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hnggoyoorle](https://clawhub.ai/user/hnggoyoorle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design or adapt a long-term memory system for AI agents, including ingestion, scoring, tree-based summarization, retrieval, and a Python MVP implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The memory design stores and reuses broad conversation data, which may include sensitive user information or credential-like content.

Mitigation: Require explicit user opt-in, redact secrets before storage, and add retention, deletion, and user/session/tenant isolation controls.

Risk: Retrieved memories can carry stale, untrusted, or prompt-injection content back into an agent conversation.

Mitigation: Inject retrieved memories only as clearly delimited untrusted context and review the skill before deployment.

## Reference(s):

- [Memory Tree MVP implementation](references/mvp-implementation.py)
- [Memory Tree quick reference](references/quick-reference.md)
- [Memory Tree quickstart](references/quickstart.md)
- [ClawHub skill page](https://clawhub.ai/hnggoyoorle/skills/memory-tree-universal)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python, SQL, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes architectural patterns, schemas, retrieval APIs, implementation cautions, and a copyable Python MVP.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
