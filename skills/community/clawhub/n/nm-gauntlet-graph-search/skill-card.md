## Description: <br>
Searches the code knowledge graph by function, class, or type using FTS5 full-text search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to search a local Gauntlet code knowledge graph for functions, classes, and types, then inspect matching source locations when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a referenced local Gauntlet/Claude Night Market graph query script that is not bundled in the artifact. <br>
Mitigation: Install only when you use and trust the referenced Gauntlet graph tooling, and review the plugin script before deployment. <br>
Risk: Search results may lead an agent to read local source files selected by the user. <br>
Mitigation: Limit use to workspaces where source inspection is intended and confirm before opening sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-gauntlet-graph-search) <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and search result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows qualified names, file paths, line numbers, and relevance scores; may offer to read a selected source file.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
