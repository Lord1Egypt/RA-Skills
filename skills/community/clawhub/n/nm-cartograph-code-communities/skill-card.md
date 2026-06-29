## Description: <br>
Detects architectural clusters and coupling boundaries via community detection on the code graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify architectural clusters, module boundaries, and high-coupling areas in Python codebases before refactoring or design review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Python project structure and imports to analyze architectural groupings. <br>
Mitigation: Install and run it only in repositories where local code-structure analysis is acceptable. <br>
Risk: The optional gauntlet path can run an existing graph_query.py from the user's local Claude plugins directory. <br>
Mitigation: Use only trusted local plugin installations and inspect the resolved graph query path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-cartograph-code-communities) <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples, tables, warnings, Mermaid diagrams, and refactoring suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an existing local gauntlet graph query when available; otherwise falls back to directory and import analysis.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
