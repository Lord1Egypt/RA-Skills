## Description:

Provides lifecycle development guidance for the Link CRM+AI Java microservice system, covering requirements analysis, technical, API, and database design, coding, testing, deployment, troubleshooting, and operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysh2ldd](https://clawhub.ai/user/ysh2ldd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, test, deploy, and operate features for the Link CRM+AI microservice system using its established Java, Spring, MyBatis, Docker, Kubernetes, and Apollo conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports live-looking internal secrets and unsafe operational guidance.

Mitigation: Do not install into a broadly shared agent environment until the publisher removes and rotates exposed Nexus credentials and the AES key, and replaces internal endpoints with placeholders or access-controlled documentation.

Risk: The skill can produce database, Kubernetes, Apollo, and signature-bypass guidance that may affect real environments.

Mitigation: Require local-only use or explicit human approval before applying generated commands, configuration changes, database changes, or signature-check exceptions.

Risk: Dependency and image sources may rely on private or insufficiently secured registries.

Mitigation: Pin and verify dependency and container image sources, and restrict private registry access to approved environments.

## Reference(s):

- [Project Architecture](references/project-architecture.md)
- [Coding Standards](references/coding-standards.md)
- [API Design Guide](references/api-design-guide.md)
- [Database Guide](references/database-guide.md)
- [Deployment Guide](references/deployment-guide.md)
- [Testing Guide](references/testing-guide.md)
- [Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, Java/XML code templates, shell commands, SQL snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before applying code, database, deployment, or operational changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
