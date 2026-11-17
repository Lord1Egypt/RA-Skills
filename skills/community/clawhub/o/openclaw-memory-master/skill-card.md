## Description:

AI memory management system that helps agents organize, analyze, retrieve, curate, and compact persistent memory with classification, tagging, deduplication, importance scoring, relation discovery, and GraphRAG-style recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent memory workflows: capturing raw memory, filtering sensitive content, compacting and curating memory files, retrieving relevant entries, scoring importance, and discovering relationships between memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent memory handling may retain private user content or sensitive personal data.

Mitigation: Use sandboxed memory paths, avoid secrets and sensitive personal data, and verify sensitive-data filtering before deployment.

Risk: Memory curation and cleanup behavior can write, update, or delete local files.

Mitigation: Review retention settings and target directories, run on test data first, and keep backups for memory stores that matter.

Risk: Security evidence reports unsafe packaging and weak controls around sensitive data.

Mitigation: Manually review package contents before install or execution, and require explicit approval for any background cleanup, migration, or file-retention task.

## Reference(s):

- [Openclaw Memory Master on ClawHub](https://clawhub.ai/cp3d1455926-svg/skills/openclaw-memory-master)
- [Artifact skill documentation](artifact/SKILL.md)
- [Development plan v4.3.0](artifact/DEV_PLAN_v4.3.0.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and JavaScript examples, shell commands, configuration notes, JSON-like analysis results, and generated memory or wiki files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist, compact, update, or delete local memory files depending on configuration and command used.]

## Skill Version(s):

4.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
