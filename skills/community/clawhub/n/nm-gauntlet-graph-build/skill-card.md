## Description: <br>
Builds or updates the code knowledge graph via tree-sitter AST and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or incrementally update a local SQLite knowledge graph for a selected codebase before search, blast-radius analysis, or flow tracing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the selected codebase and creates a local .gauntlet/graph.db index. <br>
Mitigation: Run it only on codebases the agent is allowed to inspect, and review local workspace policies before indexing sensitive repositories. <br>
Risk: The build command depends on a graph_build.py script referenced through CLAUDE_PLUGIN_ROOT that is not included in this skill artifact. <br>
Mitigation: Confirm CLAUDE_PLUGIN_ROOT points to the expected Gauntlet plugin installation before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-gauntlet-graph-build) <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local .gauntlet/graph.db SQLite index and reports parsed files, graph nodes, graph edges, and duration.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
