## Description:

Generates full-stack Java Spring Boot and Vue projects from requirements, with guided technology-stack selection, database and API scaffolding, CRUD flows, optional authentication, and setup documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallest-ming](https://clawhub.ai/user/smallest-ming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn natural-language descriptions or PRD-style requirements into scaffolded Java and Vue applications for prototypes, MVPs, and CRUD systems. It helps select a backend, database, UI library, and optional features before generating code and setup files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deployment templates can include default database usernames or passwords and published database ports.

Mitigation: Review deployment files before running them, replace default credentials, avoid root or postgres application users, and remove or restrict database port publishing.

Risk: Generated projects based on untrusted specifications may introduce unsafe code or configuration into an environment with secrets.

Mitigation: Review all generated code and deployment files before building or deploying, and keep untrusted generated projects away from secret-bearing environments.

## Reference(s):

- [Project Generator Specification Format](references/specification.md)
- [Project Generator Usage Examples](references/examples.md)
- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Vue 3 Guide](https://vuejs.org/guide/)
- [Element Plus](https://element-plus.org/)
- [Ant Design Vue](https://antdv.com/)
- [Naive UI](https://www.naiveui.com/)
- [MyBatis Spring Boot](https://mybatis.org/spring-boot-starter/)
- [Flyway Documentation](https://documentation.red-gate.com/flyway/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses plus generated project files and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files vary by selected Java, Spring Boot, database, Vue, UI library, and optional feature choices.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
