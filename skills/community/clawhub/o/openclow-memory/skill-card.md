## Description: <br>
OpenClaw long-term memory system that supports structured PostgreSQL memory, vector memory, and semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damienCronw](https://clawhub.ai/user/damienCronw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve long-term agent context, preferences, decisions, goals, and reference material in local databases and retrieve it through structured or semantic search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private local memory files may be copied into persistent PostgreSQL storage. <br>
Mitigation: Review the scripts before use, avoid storing highly sensitive memories, and add explicit review and deletion controls for archived data. <br>
Risk: Database access may expose long-term memories if broad credentials are used. <br>
Mitigation: Use a dedicated least-privileged PostgreSQL user for the memory databases. <br>
Risk: Search results may reveal or surface retained memories unexpectedly. <br>
Mitigation: Install only when a local long-term memory system is intended and periodically review retained memory content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/damienCronw/openclow-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local PostgreSQL, pgvector, local memory files, psql, and a local embedding endpoint when the included scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
