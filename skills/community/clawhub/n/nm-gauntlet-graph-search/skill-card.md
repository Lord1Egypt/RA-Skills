## Description: <br>
Searches the code knowledge graph by function, class, or type using FTS5 full-text search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to search a prebuilt Gauntlet code knowledge graph for functions, classes, and types, then inspect matching source locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some release workflows described by the security evidence can send data to external review tools or perform administrative or production changes when explicitly invoked. <br>
Mitigation: Install and invoke the skill only when those workflows are expected, and require operator review before moderation, email, migration, autoreview, administrative, or production-changing actions. <br>
Risk: The graph search command depends on an existing .gauntlet/graph.db database. <br>
Mitigation: Build the graph first, such as with the related graph-build workflow, before relying on search results. <br>


## Reference(s): <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and search result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include qualified names, file paths, line numbers, and relevance scores when the graph query succeeds.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
