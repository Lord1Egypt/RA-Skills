## Description:

Generates architecture diagrams, flowcharts, dependency graphs, state machines, and other visualizations from natural language as Graphviz DOT with a clickable GraphvizOnline preview link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redf426](https://clawhub.ai/user/redf426)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and technical teams use this skill to turn natural-language descriptions of systems, flows, schemas, dependencies, and state machines into Graphviz DOT diagrams with an online preview link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOT content is embedded in a GraphvizOnline URL and opened in a third-party web page.

Mitigation: Do not include secrets, credentials, private schemas, or sensitive internal architecture in diagrams intended for online rendering.

Risk: Generated diagrams may omit details or misrepresent relationships from the user's description.

Mitigation: Review the DOT source and rendered diagram before relying on it for design, documentation, or implementation decisions.

## Reference(s):

- [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Superpowers plugin](https://github.com/nicobailon/superpowers-claude-code)
- [ClawHub skill page](https://clawhub.ai/redf426/skills/graphviz-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with a fenced DOT code block and clickable GraphvizOnline link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DOT source is URL-encoded into a GraphvizOnline hash fragment for rendering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
