## Description: <br>
Builds or updates the code knowledge graph via tree-sitter AST and SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to build or refresh a local code knowledge graph before code search, blast-radius analysis, flow tracing, or structure-oriented questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates local .gauntlet files in the selected repository. <br>
Mitigation: Confirm the target repository or path before running the build. <br>
Risk: Running against the wrong workspace can produce a graph for unintended source files. <br>
Mitigation: Point the agent at the repository you intend to index before invoking the build. <br>


## Reference(s): <br>
- [Nm Gauntlet Graph Build on ClawHub](https://clawhub.ai/athola/nm-gauntlet-graph-build) <br>
- [Gauntlet homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, json, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .gauntlet files, including a SQLite graph database and gitignore.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
