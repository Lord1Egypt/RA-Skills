## Description:

Build and maintain a persistent Logseq data architecture, based on the characteristics of bidirectional link technology, divided into three layers: raw data, index files, and rule files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesopodamia](https://clawhub.ai/user/mesopodamia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize a Logseq knowledge base into raw material, index, and rule layers; generate Markdown summaries, entity pages, concept pages, cross-references, and query answers; and run health checks on the resulting graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad authority to create and update persistent Logseq notes and indexes.

Mitigation: Use it on a backed-up or version-controlled Logseq graph and require dry-run or read-only review before approving writes.

Risk: Artifact behavior conflicts on whether raw source materials are immutable or may be modified.

Mitigation: Keep raw source materials outside agent-writable paths or explicitly require user approval before any raw material edits.

Risk: Archiving casual questions as pages can persist private or sensitive information in the knowledge base.

Mitigation: Require confirmation before archiving answers and avoid saving private questions or source material unless the user explicitly approves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mesopodamia/skills/logseq-article-archive)
- [Publisher profile](https://clawhub.ai/user/mesopodamia)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact maintenance rules](artifact/RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown pages, Logseq bidirectional links, structured reports, and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Logseq index pages, summaries, entity pages, concept pages, comparison tables, health reports, and log entries.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
