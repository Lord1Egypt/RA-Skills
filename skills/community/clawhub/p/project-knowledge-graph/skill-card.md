## Description: <br>
Cross-project knowledge graph powered by local FalkorDB that indexes project artifacts across configured projects and lets agents query them by concept. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelvillar1](https://clawhub.ai/user/adelvillar1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to build and query a local cross-project memory index for recaps, plans, project memory files, architecture documents, and skill files. It helps surface prior decisions and related implementation context across configured projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a persistent local index of configured project roots and installed skills, which may retain sensitive or stale project content. <br>
Mitigation: Run the dry-run first, exclude sensitive project roots before indexing, and purge or rebuild the local index when source content should no longer be searchable. <br>
Risk: Changing the FalkorDB host away from localhost can send indexed project data to a remote database. <br>
Mitigation: Keep the FalkorDB host set to localhost unless the remote host is intentional and trusted; treat the script's remote-host prompt as a required review point. <br>
Risk: Deletion commands can remove local indexed chunks, including full-index removal with delete --all. <br>
Mitigation: Prefer scoped deletion by project or document type when possible, and confirm the intended index target before running full-index deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adelvillar1/project-knowledge-graph) <br>
- [Publisher profile](https://clawhub.ai/user/adelvillar1) <br>
- [Publisher homepage](https://github.com/adelvillar1) <br>
- [Backend Storage Evaluation: SQLite vs FalkorDB](references/falkordb-vs-sqlite-evaluation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local indexing, query, health-check, statistics, and deletion command guidance for a FalkorDB-backed project knowledge graph.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact frontmatter lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
