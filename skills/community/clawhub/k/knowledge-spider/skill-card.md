## Description:

本地知识库 stores, queries, deletes, and summarizes local user preferences, facts, tasks, and other information for agent reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toughspider](https://clawhub.ai/user/toughspider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain a local knowledge base of user preferences, facts, tasks, and important notes, then retrieve relevant entries for more personalized responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local knowledge-base records can persist sensitive content in plaintext.

Mitigation: Do not store passwords, tokens, keys, or private personal data; review stored records before relying on them.

Risk: Deletion and automatic context reuse may occur without enough safeguards.

Mitigation: Confirm deletion targets and review retrieved context before reusing it in agent responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toughspider/skills/knowledge-spider)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON tool responses with natural-language or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include stored content, categories, counts, metadata, and context snippets from a local persistent knowledge base.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
