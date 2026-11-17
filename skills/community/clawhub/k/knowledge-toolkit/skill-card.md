## Description:

本地知识库集成 helps agents search, ingest, and switch modes for a local knowledge base so users can manage documents and retrieve information more efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent operators, and enterprise teams use this skill to search local documents, ingest documents into a local knowledge base, and switch between local retrieval and conversational knowledge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read and store local document contents beyond the user's intended scope.

Mitigation: Limit use to an explicitly chosen knowledge-base folder, avoid sensitive files, and review documents before ingestion.

Risk: Broad triggers and command-capable behavior may start ingestion or actions without enough context.

Mitigation: Require explicit confirmation before document ingestion or command execution, and review proposed actions before allowing writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional JSON status blocks and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local document search, ingestion, mode switching, and configuration steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
