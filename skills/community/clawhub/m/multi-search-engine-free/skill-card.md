## Description:

搜索引擎 helps an agent use multiple Chinese and global search providers to gather, compare, and summarize web search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to request multi-engine web searches, compare results across regional and global sources, and produce concise search summaries or structured findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests broad local read and command-execution capabilities for a search-oriented workflow.

Mitigation: Install only in environments where those permissions are acceptable, and avoid using the skill with secrets, confidential search terms, private files, or credentials.

Risk: Search results can include misleading, unsafe, or stale external content.

Mitigation: Review important results against trusted sources before relying on them for decisions or downstream automation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown or structured JSON examples with inline commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the agent runtime, enabled network access, and selected search providers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
