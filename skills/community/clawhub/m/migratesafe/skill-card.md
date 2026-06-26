## Description: <br>
MigrateSafe checks database migration files for destructive operations before they reach production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan SQL, Rails, Django, Knex.js, Prisma, Flyway, and Liquibase migrations for destructive operations, missing rollbacks, lock hazards, and risky schema changes before deployment or commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid features read MIGRATESAFE_LICENSE_KEY or the local OpenClaw configuration file. <br>
Mitigation: Store the license key as a secret and review local configuration access before enabling Pro or Team commands. <br>
Risk: The hooks install command changes the current repository's lefthook configuration and may block commits with high-risk staged migrations. <br>
Mitigation: Run hooks install only inside the intended repository, review lefthook.yml changes, and keep uninstall or bypass decisions aligned with project policy. <br>
Risk: The report command may create a markdown compliance report in the working directory. <br>
Mitigation: Run report from an appropriate project directory and review generated reports before sharing them. <br>


## Reference(s): <br>
- [MigrateSafe ClawHub page](https://clawhub.ai/suhteevah/migratesafe) <br>
- [MigrateSafe homepage](https://migratesafe.pages.dev) <br>
- [Lefthook](https://github.com/evilmartians/lefthook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, markdown reports, and shell command or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results can include file paths, line numbers, severities, operations, recommendations, risk scores, and exit codes; paid commands may write lefthook configuration or markdown reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact scripts report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
