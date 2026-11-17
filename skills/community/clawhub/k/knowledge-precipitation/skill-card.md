## Description:

每日知识沉淀引擎（Knowledge Auto-Precipitation Engine，KAPE）generates a structured daily knowledge briefing from GetNote notes and conversation history, then archives it locally and to GetNote and Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or personal knowledge-management users use this skill to turn the previous day's notes and conversations into a complete Chinese daily briefing with themes, insights, keywords, and follow-up focus areas. It is intended for workflows that deliberately sync the resulting briefing into GetNote and Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests access to private conversations, GetNote content, and local OpenClaw secret files.

Mitigation: Install only for the intended personal workflow, remove direct secret-file reads, and avoid logging credential prefixes or other secret material.

Risk: The skill uploads generated briefings to external GetNote and Feishu destinations and grants a fixed Feishu account full control.

Mitigation: Require explicit user approval before each external sync or permission change, and remove hard-coded Feishu recipients, folder tokens, and account-specific sharing rules before use.

Risk: The artifact understates side effects compared with the server security summary.

Mitigation: Require a local preview of the generated briefing and a clear destination list before any write, share, delete, or sync operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binhuatochina/skills/knowledge-precipitation)
- [Briefing template](artifact/references/briefing-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefing with command-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a daily Chinese briefing and sync-status summary; Feishu document writes may require XML formatting for tables.]

## Skill Version(s):

0.1.18 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
