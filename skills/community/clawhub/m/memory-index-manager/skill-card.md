## Description:

记忆索引系统。用于管理长期项目记忆、自动维护索引、快速定位历史项目。仅在用户明确说"回忆一下""remember""recall"时触发读取，写入与OpenClaw原生机制保持一致，索引维护在后台自动进行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxc159620352](https://clawhub.ai/user/zxc159620352)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain a topic index over long-running project memory, recover prior context on explicit recall requests, and consolidate older memory entries into durable Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process long-term memory that may contain sensitive personal, business, or credential-adjacent information.

Mitigation: Review memory contents and workspace trust boundaries before enabling indexing or consolidation.

Risk: The daily flush design can perform scheduled background memory maintenance without a direct user prompt.

Mitigation: Keep scheduled flush setup opt-in, auditable, and easy to disable or remove.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxc159620352/skills/memory-index-manager)
- [Publisher profile](https://clawhub.ai/user/zxc159620352)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses plus memory index and consolidation file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads memory on explicit recall triggers; background maintenance may update index and consolidation files.]

## Skill Version(s):

2.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
