## Description: <br>
Generates a full men's fashion e-commerce project with Spring Boot 3, Vue 3, and MySQL, including a confirmed technical plan followed by backend, frontend, database, API, and deployment artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtbian](https://clawhub.ai/user/wtbian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to plan and generate a men's fashion e-commerce web application with product, user, cart, order, payment, inventory, logistics, and marketing modules. It is aimed at creating a runnable full-stack project scaffold and supporting documentation for further review and customization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated configuration examples include unsafe database credentials and static JWT secrets. <br>
Mitigation: Replace root/123456 and static JWT secrets with environment-managed values before running or deploying generated code. <br>
Risk: Database cleanup and backup-pruning examples can delete data if run without review. <br>
Mitigation: Use a dedicated development workspace, avoid production databases, and review backups, affected-row counts, and retention policy before running cleanup commands. <br>
Risk: Generated files may be incomplete or unsuitable for production without security review. <br>
Mitigation: Review and scan generated files before execution, especially payment, authentication, database, and deployment configuration. <br>


## Reference(s): <br>
- [Backend Architecture](artifact/references/backend-architecture.md) <br>
- [Frontend Architecture](artifact/references/frontend-architecture.md) <br>
- [Frontend Architecture Continued](artifact/references/frontend-architecture-continued.md) <br>
- [Database Schema](artifact/references/database-schema.md) <br>
- [Database Schema Continued](artifact/references/database-schema-continued.md) <br>
- [API Specification](artifact/references/api-specification.md) <br>
- [API Specification Continued](artifact/references/api-specification-continued.md) <br>
- [Usage Example](artifact/examples/usage-example.md) <br>
- [ClawHub Release Page](https://clawhub.ai/wtbian/mens-fashion-ecommerce) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated project files, shell scripts, SQL, Java, Vue, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Two-stage workflow: first produce a technical plan for user confirmation, then generate the project implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
