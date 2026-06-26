## Description: <br>
Detects architectural clusters and coupling boundaries via community detection on the code graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to identify architectural clusters, module boundaries, coupling hotspots, and refactoring targets in a codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architectural clusters and coupling warnings may be incomplete or misleading when graph data is missing or stale. <br>
Mitigation: Review the generated analysis against the current codebase before making refactoring decisions. <br>
Risk: The skill can propose shell commands that inspect local source files and depend on optional gauntlet tooling. <br>
Mitigation: Run commands only in the intended repository and confirm optional tool paths before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-cartograph-code-communities) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command snippets, tables, warnings, and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use gauntlet graph data when available and falls back to directory and import analysis.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
