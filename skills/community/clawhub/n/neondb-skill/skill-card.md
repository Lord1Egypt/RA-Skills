## Description:

Manage Neon serverless Postgres databases, including projects, branches, databases, connection strings, and SQL queries through the Neon CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbot-ved](https://clawhub.ai/user/clawbot-ved)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to provision and manage Neon serverless Postgres projects, create database branches for development or experiments, retrieve connection strings, and run SQL workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle real Neon credentials and may expose database connection strings in terminal output or logs.

Mitigation: Use test projects where possible, avoid logged environments for setup, and rotate any exposed connection string or API key.

Risk: The documented workflows include destructive database operations such as project, branch, database, reset, export, and import commands.

Mitigation: Require explicit approval before destructive operations and confirm project, branch, and database targets before execution.

## Reference(s):

- [Neon homepage](https://neon.tech)
- [Neon Console](https://console.neon.tech)
- [Neon API documentation](https://api-docs.neon.tech)
- [Neon CLI reference](https://neon.tech/docs/reference/neon-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline bash, SQL, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Neon project identifiers, connection strings, CLI output format choices, and database setup commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
