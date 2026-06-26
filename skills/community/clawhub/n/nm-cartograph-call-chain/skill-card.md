## Description: <br>
Traces execution paths through the code graph with criticality scoring and Mermaid charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to trace how functions or entry points propagate through a codebase, review call-chain criticality, and produce Mermaid diagrams for inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to read and analyze local repository code and may run a local graph_query.py helper when an existing gauntlet plugin is available. <br>
Mitigation: Use it only in repositories where code inspection is acceptable, review proposed commands before execution, and avoid running it on sensitive codebases without approval. <br>


## Reference(s): <br>
- [Cartograph homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-call-chain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with indented call trees, Mermaid diagrams, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local graph_query.py helper when the gauntlet plugin is installed; otherwise falls back to static code search.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence and target metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
