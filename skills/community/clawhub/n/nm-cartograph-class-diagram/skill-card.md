## Description: <br>
Generates a Mermaid class diagram showing types, inheritance, and composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a codebase and produce a concise Mermaid class diagram of public types, inheritance, composition, and related relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read scoped code structure and pass diagram content to a configured Mermaid rendering tool. <br>
Mitigation: Invoke it only on code you are comfortable having structurally analyzed and rendered through that tool, especially for private repositories. <br>
Risk: Generated diagrams may omit detail because the workflow intentionally limits diagrams to 12-15 classes and public members. <br>
Mitigation: Review the selected scope and diagram output before relying on it for architecture or API documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-class-diagram) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown containing Mermaid classDiagram code and analysis notes, with optional rendered diagram output from a Mermaid MCP tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits diagrams to 12-15 classes and focuses on public methods, key attributes, inheritance, composition, aggregation, and dependencies.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
