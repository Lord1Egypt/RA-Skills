## Description: <br>
Helps design backend business solutions and technical implementation plans, including project analysis, architecture design, Mermaid diagrams, Go-style gRPC/HTTP API contracts, and MySQL schema drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjjypink1211](https://clawhub.ai/user/jjjypink1211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and backend engineers use this skill to turn business requirements or scoped existing projects into architecture notes, business process diagrams, interface contracts, and database table designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Engineering-analysis mode may read project files that include secrets or unrelated private data if the user provides an overly broad path. <br>
Mitigation: Use a scoped project directory and exclude secrets or unrelated private files before asking the agent to analyze an existing codebase. <br>
Risk: Architecture, API, and database designs are generated guidance and may be incomplete or mismatched to production constraints. <br>
Mitigation: Review generated designs with project owners before implementation and validate security, reliability, and data-model choices against the target system. <br>


## Reference(s): <br>
- [Common Business Scenario Design Patterns](references/patterns.md) <br>
- [Architecture Design Patterns](references/architecture-patterns.md) <br>
- [Mermaid Diagram Syntax Quick Reference](references/mermaid-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Mermaid diagrams, protobuf-style API definitions, SQL snippets, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read scoped project files when the user requests engineering analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
