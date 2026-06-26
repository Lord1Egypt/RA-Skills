## Description: <br>
Validates SQL syntax of pending database migration files before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to check pending SQL migration files before execution, including CI/CD gate checks and change-control review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator reads the configured migrations directory and SQLite migration table, so incorrect paths can expose unintended local project data. <br>
Mitigation: Set migrations_dir and db_path deliberately and run the skill in CI or another controlled workspace against the intended project data. <br>
Risk: The validator executes local migration SQL in an in-memory SQLite database for syntax validation. <br>
Mitigation: Validate only trusted migration files and review validation errors before promoting migrations into an execution pipeline. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ink5725/migration-validator) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON validation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports discovered migrations, applied and pending migration lists, validation errors, timestamp, and completion status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
