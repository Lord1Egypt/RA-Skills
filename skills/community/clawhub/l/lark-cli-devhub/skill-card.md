## Description:

Lark CLI Dev Hub helps developers use lark-cli or feishu-cli to keep Feishu/Lark project knowledge, bugfix memory, task state, release evidence, pitfalls, and AI run summaries current.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to search, record, and route project knowledge in Feishu/Lark while working on bugs, AI run summaries, releases, and main-branch writeback discipline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may write sensitive project details into Feishu/Lark records or local outbox payloads.

Mitigation: Review payloads before writeback and keep secrets, tokens, private keys, raw credentials, and full environment files out of records and outbox items.

Risk: Writeback gates can disrupt commit or push workflows if enforcement is enabled before the team trusts the process.

Mitigation: Use shadow mode first, confirm receipt and outbox behavior, and switch to enforced mode only after the workflow is reliable.

Risk: A failed Feishu/Lark write can leave project knowledge incomplete if treated as successful.

Mitigation: Leave a Dev Hub outbox item after failed writes and sync it later instead of reporting a completed writeback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afengzi/skills/lark-cli-devhub)
- [Knowledge Model](references/knowledge-model.md)
- [Writeback Flows](references/writeback-flows.md)
- [Hook Policy](references/hook-policy.md)
- [Domain Map](references/domain-map.md)
- [Search Policy](references/search-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires lark-cli, python3, and git; may create Dev Hub receipts or outbox items for project writeback tracking.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
