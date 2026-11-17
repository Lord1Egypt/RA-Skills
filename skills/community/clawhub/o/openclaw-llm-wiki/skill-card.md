## Description:

Create and maintain a persistent LLM-maintained knowledge base (wiki) following Andrej Karpathy's pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pathanaawej0-dot](https://clawhub.ai/user/pathanaawej0-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to have an agent initialize, populate, query, and maintain a local markdown wiki from curated source documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source documents, summaries, derived wiki pages, and query logs may persist sensitive information in the workspace.

Mitigation: Only place documents in llm-wiki/raw/ when persistent local storage is acceptable, and review generated wiki pages and logs before sharing or committing the workspace.

Risk: The agent may modify local wiki files while ingesting or maintaining knowledge.

Mitigation: Ask the agent to identify the files it will read or update and preview planned wiki changes before ingestion or maintenance in important repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update a local llm-wiki directory, including raw source storage, wiki pages, an index, logs, and schema guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
