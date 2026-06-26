## Description: <br>
Generates a Mermaid workflow diagram showing process steps, decisions, and state transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect selected code or documentation and turn workflows, CI/CD pipelines, lifecycle processes, or state machines into Mermaid flowcharts with a short explanation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose selected project structure and generated Mermaid content to the configured Mermaid Chart MCP renderer. <br>
Mitigation: Use it only with a trusted renderer and avoid sensitive code paths unless the diagram content is acceptable to share with that renderer. <br>
Risk: Generated workflow diagrams can omit or simplify process steps, decisions, or state transitions. <br>
Mitigation: Review the Mermaid diagram and short explanation against the source workflow before relying on it for documentation or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-workflow-diagram) <br>
- [Cartograph source homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Mermaid code and a brief prose summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow asks the agent to render Mermaid through the configured Mermaid Chart MCP tool when available.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
