## Description:

Writes, debugs, and reviews PHP code and configuration across type handling, arrays, OOP, Composer, PDO, sessions, PHP-FPM, OPcache, PHP 8 features, testing, static analysis, security, and deployment troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write and review PHP, diagnose runtime and deployment failures, harden web boundaries, and produce PHP code, configuration, tests, shell commands, and review guidance for common PHP application work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying generated production PHP-FPM configuration without review may expose more environment variables than intended.

Mitigation: Review environment-variable exposure before deployment, especially clear_env = no, and prefer explicitly forwarding only the variables the application needs.

## Reference(s):

- [ClawHub PHP skill page](https://clawhub.ai/ivangdavila/skills/php)
- [Clawic PHP skill page](https://clawic.com/skills/php)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PHP snippets, Composer commands, php.ini or PHP-FPM configuration, PHPUnit/PHPStan setup, and review checklists.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
