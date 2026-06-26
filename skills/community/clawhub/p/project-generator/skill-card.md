## Description: <br>
Generates full-stack Java Spring Boot and Vue projects from requirements with guided technology stack selection for database, API, authentication, and UI choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallest-ming](https://clawhub.ai/user/smallest-ming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn requirements, PRDs, or feature lists into Java/Vue application scaffolds, generated backend and frontend code, database schema, configuration, and setup documentation after confirming a technology stack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated database and Docker Compose templates may contain unsafe defaults for production, including default passwords, privileged database accounts, or public port mappings. <br>
Mitigation: Review generated configuration before running it, replace default credentials, avoid superuser application accounts, remove unnecessary public database ports, and enable appropriate transport security. <br>
Risk: Generated project dependencies and configuration are scaffolding and may not include deployment-ready lockfiles, audits, or environment-specific hardening. <br>
Mitigation: Create lockfiles, audit dependencies, and apply the organization's security and deployment requirements before using generated projects beyond local development. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smallest-ming/project-generator) <br>
- [Project Generator Specification Format](references/specification.md) <br>
- [Project Generator Usage Examples](references/examples.md) <br>
- [Spring Boot Reference Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/) <br>
- [Vue Guide](https://vuejs.org/guide/) <br>
- [MyBatis Spring Boot Starter](https://mybatis.org/spring-boot-starter/) <br>
- [Flyway Documentation](https://documentation.red-gate.com/flyway/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with generated project files, code snippets, configuration files, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the user for requirements and explicit technology stack choices before generation; generated database, Docker, and application configuration should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
