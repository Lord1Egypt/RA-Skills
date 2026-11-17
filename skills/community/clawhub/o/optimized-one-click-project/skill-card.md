## Description:

Generates and starts a configurable Spring Boot and Vue 3 CRUD application with RBAC scaffolding, database initialization, optional Redis and Swagger support, and browser launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallest-ming](https://clawhub.ai/user/smallest-ming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate a full-stack administrative CRUD project from JSON configuration, including backend APIs, Vue management pages, database setup, and local startup commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated applications may include unsafe authentication, weak token handling, plaintext or default credentials, and unprotected data-changing APIs.

Mitigation: Review and harden authentication, authorization, token handling, and credential storage before using generated applications with real users or data.

Risk: Database initialization may reset or destructively modify local database state.

Mitigation: Run only against disposable local databases until the SQL initialization behavior has been reviewed and adjusted.

Risk: The skill can install dependencies and launch generated backend and frontend services automatically.

Mitigation: Execute it in an isolated development environment, review generated commands and dependencies, and avoid exposing services until the application has been secured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallest-ming/skills/optimized-one-click-project)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates Spring Boot, Vue 3, SQL, Maven, and npm assets and may start local services.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
