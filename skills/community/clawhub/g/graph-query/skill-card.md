## Description:

Routes blockchain data questions to Graph Protocol services for real-time analysis, subgraph selection, and GraphQL query optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and automation users use this skill to ask blockchain data questions, choose relevant Graph Protocol subgraphs, and receive query optimization or reporting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command execution authority for a Graph Protocol helper.

Mitigation: Install only in agent environments where command execution and filesystem access can be restricted or reviewed.

Risk: The security verdict is suspicious because the declared authority and some instructions are broader or mismatched for the stated purpose.

Mitigation: Review the skill before installation and keep execution scoped to blockchain query routing, subgraph selection, and query optimization tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/graph-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 2.9.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
