## Description: <br>
Preflight Prisma migration state before deploy; fails fast on drift, failed migrations, missing DB URLs, or unapplied migration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill before CI release steps or deployments to check that Prisma migration state is healthy before deploy or startup migration steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured database URL could point to the wrong environment when used as a deploy gate. <br>
Mitigation: Verify the selected environment variable and target database before enabling this check in CI or deployment workflows. <br>
Risk: The Prisma CLI invoked through npx can vary if the project or CI environment does not pin dependencies. <br>
Mitigation: Use the project's pinned Prisma dependency or a locked CI install for repeatable migration status checks. <br>
Risk: Allowing drift or unapplied migrations can turn blocking findings into warnings. <br>
Mitigation: Use PRISMA_MIGRATE_GUARD_ALLOW_DRIFT and PRISMA_MIGRATE_GUARD_ALLOW_UNAPPLIED only for explicitly approved workflows. <br>


## Reference(s): <br>
- [Prisma Migrate Guard on ClawHub](https://clawhub.ai/daniellummis/prisma-migrate-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text PASS/WARN/FAIL report with shell exit code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 indicates healthy migration status; exit code 1 indicates blocking migration issues.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
