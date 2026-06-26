## Description: <br>
Discover and structure product opportunities from public user discussions, then convert top opportunities into a lightweight PRD for a coding agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao-weijie](https://clawhub.ai/user/zhao-weijie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, product builders, and coding agents use this skill to find recurring public user pain points, rank product opportunities, and turn a persisted opportunity into a lightweight PRD. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists public-source evidence, opportunity analyses, and PRDs in a user-configured TiDB database. <br>
Mitigation: Use a database you control, configure `TIDB_DATABASE_URL` carefully, and define retention and deletion practices before storing sensitive strategy work. <br>
Risk: Confidential product strategy could be stored if users provide it during discovery or PRD generation. <br>
Mitigation: Avoid entering confidential strategy unless the database and access controls meet your organization's requirements. <br>


## Reference(s): <br>
- [Painpoint To PRD Contracts](references/contracts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhao-weijie/pain2mvp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, lightweight PRDs, JSON payloads, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists evidence, opportunity snapshots, and PRDs in a user-configured TiDB database.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
