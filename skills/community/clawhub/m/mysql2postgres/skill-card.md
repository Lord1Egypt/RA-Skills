## Description:

Use this skill when migrating a project's database layer from MySQL to PostgreSQL; it covers SQL dialect conversion, MyBatis/MyBatis-Plus configuration, JDBC setup, data type pitfalls, and common runtime error fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawrencehe](https://clawhub.ai/user/lawrencehe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and review Java Spring Boot/MyBatis migrations from MySQL to PostgreSQL, including SQL rewrite patterns, ORM configuration, JDBC settings, sequences, and runtime error fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database migration changes can affect production data if suggested SQL replacements or sequence creation are applied without schema-specific review.

Mitigation: Review suggested SQL replacements and sequence creation against the target schema before applying them.

Risk: The migration reference is written in Chinese, which may increase misunderstanding risk for readers who are not comfortable with the language.

Mitigation: Install and use the skill only when the team is comfortable using a Chinese-language migration reference.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lawrencehe/skills/mysql2postgres)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with SQL, YAML, and Java examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language migration reference; produces advisory guidance rather than executable code.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
