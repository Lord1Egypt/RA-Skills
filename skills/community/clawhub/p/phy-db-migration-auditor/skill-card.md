## Description: <br>
Database migration safety auditor that parses Alembic, Flyway, Django, Rails ActiveRecord, and Prisma migrations to classify operation risk, check rollback coverage, flag backward compatibility issues, detect lock-escalating changes, and generate deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database owners use this skill to review schema migrations before deployment, identify risky operations that may cause downtime or data loss, and produce pre-deploy checklists or rollback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads migration and related source or model files in the target repository. <br>
Mitigation: Install only when repository file access is acceptable for the agent and its execution environment. <br>
Risk: Rollback scripts and production migration recommendations are advisory and may be incomplete for a specific database or deployment process. <br>
Mitigation: Have a database owner review generated rollback scripts and production recommendations before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-db-migration-auditor) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables, checklists, inline shell commands, and rollback code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file analysis only; no external API calls are described by the release evidence.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
