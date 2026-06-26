## Description: <br>
Generates Graphviz DOT diagrams from natural language descriptions and returns a clickable GraphvizOnline preview link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redf426](https://clawhub.ai/user/redf426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and technical teams use this skill to turn architecture, flowchart, dependency, state-machine, schema, and ER-diagram requests into Graphviz DOT diagrams with online previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram content embedded in a GraphvizOnline link may expose sensitive architecture, hostnames, schemas, credentials, or unreleased system details to a third-party-rendered preview. <br>
Mitigation: Do not include secrets or sensitive internal details in generated diagrams unless they are intended for online rendering; use local Graphviz rendering for sensitive diagrams. <br>


## Reference(s): <br>
- [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Superpowers plugin](https://github.com/nicobailon/superpowers-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with a short description, fenced DOT code block, and clickable GraphvizOnline link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [DOT source is URL-encoded into a GraphvizOnline hash-fragment preview link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
