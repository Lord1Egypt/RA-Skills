## Description: <br>
Generates a Mermaid sequence diagram showing how data moves between components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to trace request flows, understand data transformation pipelines, and document API call chains as Mermaid sequence diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect code in the user-selected scope. <br>
Mitigation: Use it only on repositories and scopes that are appropriate for agent-assisted analysis. <br>
Risk: Generated Mermaid diagram content may be sent to a configured Mermaid Chart MCP for rendering. <br>
Mitigation: Avoid including sensitive code details in diagram prompts unless that renderer is approved for the data. <br>


## Reference(s): <br>
- [Cartograph plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-data-flow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Mermaid sequence diagram code blocks and brief prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May validate and render generated Mermaid content with the configured Mermaid Chart MCP.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
