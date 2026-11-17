## Description:

Manage an Obsidian-based personal knowledge base (wiki) with strict ingestion, query, lint, reflect, merge, and system maintenance protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haima666](https://clawhub.ai/user/haima666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage an Obsidian personal knowledge base, including source ingestion, knowledge retrieval, wiki health checks, synthesis, deduplication, and question tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary questions can trigger local commands and persistent Obsidian vault edits.

Mitigation: Install only when the agent is allowed to read the user's Obsidian raw/wiki content, write wiki pages and reports, and run local qmd maintenance commands.

Risk: Generated wiki destinations or reports may write content to the wrong location.

Mitigation: Use explicit command phrases and review generated destinations before saving.

Risk: Local qmd invocations may be exposed to unsafe query handling.

Mitigation: Ensure any qmd invocation passes user queries as literal arguments rather than through shell interpolation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured tables, bullet lists, code blocks, and local file update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent Obsidian vault edits and local qmd maintenance commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
