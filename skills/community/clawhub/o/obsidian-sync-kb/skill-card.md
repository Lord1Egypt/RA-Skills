## Description:

Build a searchable local knowledge base from an Obsidian vault's "笔记同步助手" inbox, then answer with citations, topic cards, update logs, and daily digests for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangkaifeng](https://clawhub.ai/user/pangkaifeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn a synced Obsidian inbox into a retrieval-ready local knowledge base. It supports index building, cited question answering, topic promotion, update logs, and daily digests for OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send note-derived data to the web by default and fetch URLs found in notes.

Mitigation: Review the target vault before use and run builds with --disable-network or set research.enable_network to false unless network enrichment is intended.

Risk: Private, client, work, or internal research notes may be indexed or used as source material.

Mitigation: Use the skill only on approved vaults and confirm that generated citations, topic cards, logs, and digests do not expose sensitive note content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with cited excerpts, optional JSON query results, and shell commands or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local index, state, topic-card, update-log, and daily-digest files under configured vault directories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
