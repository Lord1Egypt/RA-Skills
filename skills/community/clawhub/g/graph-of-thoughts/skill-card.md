## Description: <br>
Graph-based reasoning with thought combination and feedback loops for exploring multiple solution paths, combining insights, and synthesizing optimal solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to structure complex reasoning tasks that need multiple candidate approaches, cross-path synthesis, feedback loops, and final solution aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated solutions or execution examples could be treated as ready-to-run actions without adequate review. <br>
Mitigation: Review generated reasoning outputs and any proposed commands or code before execution or deployment. <br>
Risk: Cache or memory examples could retain sensitive problem details if adapted without retention controls. <br>
Mitigation: Avoid using cache or memory patterns with sensitive inputs unless storage scope, retention, and deletion controls are defined. <br>
Risk: The wrapper code is incomplete and should not be assumed to provide a production implementation. <br>
Mitigation: Treat wrapper behavior as illustrative unless the implementation is completed, tested, and reviewed separately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobisamaa/graph-of-thoughts) <br>
- [Integration guide](INTEGRATION.md) <br>
- [Quick reference](QUICKREF.md) <br>
- [Examples overview](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured reasoning templates, tables, code blocks, shell command examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated thought graphs, path evaluations, combined solutions, feedback iterations, and verification checklists.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
