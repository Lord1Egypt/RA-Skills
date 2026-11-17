## Description:

Guides developers in designing reusable .NET Web API services with layered architecture, data access, authentication, API documentation, logging, and supporting libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weslon1987](https://clawhub.ai/user/weslon1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and scaffold .NET Web API applications, including clean architecture, SqlSugar data access, JWT authorization, versioned API documentation, and Serilog logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied JWT examples may grant overly broad permissions or omit resource-owner checks.

Mitigation: Review generated authorization code; load permission claims from the authorization store and verify resource ownership and policy names before use.

Risk: Logging examples may expose sensitive request data or tokens.

Mitigation: Review request-logging configuration and redact sensitive fields; do not log full request bodies or tokens in production.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/weslon1987/skills/net-full-stack-architect)
- [Project structure and scaffolding](references/project-structure.md)
- [SqlSugar ORM integration](references/orm-sqlsugar.md)
- [JWT authentication and authorization](references/auth-jwt.md)
- [API documentation and versioning](references/api-docs-versioning.md)
- [Serilog logging](references/logging-serilog.md)
- [Third-party library selection](references/third-party-libraries.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands, Markdown]

**Output Format:** [Markdown with architecture notes, code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a scaffold and a sample CRUD implementation.]

## Skill Version(s):

1.0.1 (source: ClawHub release; skill frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
