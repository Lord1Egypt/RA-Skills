## Description: <br>
Generates a Mermaid dependency graph showing import relationships between modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect project imports and produce Mermaid dependency diagrams for coupling analysis, circular dependency checks, and refactor planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repository structure and import relationships, which can expose sensitive architecture details if the requested scope is too broad. <br>
Mitigation: Limit analysis to the modules needed for the task and avoid including private package names or architecture details in shared outputs. <br>
Risk: Rendering Mermaid diagrams through an external MCP renderer may disclose module names or dependency structure. <br>
Mitigation: Use local rendering or omit external rendering when diagrams contain private repository structure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-dependency-graph) <br>
- [Cartograph source homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, guidance] <br>
**Output Format:** [Markdown with Mermaid flowchart code and analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dependency counts, fan-in and fan-out notes, and circular dependency observations.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
