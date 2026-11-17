## Description:

Build production Spring Boot applications - REST APIs, Security, Data, Actuator

This skill is ready for commercial/non-commercial use.

## Publisher:

[watermelon11](https://clawhub.ai/user/watermelon11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and review production-oriented Spring Boot applications, including REST APIs, Spring Security, Spring Data, Actuator monitoring, and cloud integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Spring Security examples can weaken protections if copied without adapting CSRF, authentication, or route rules.

Mitigation: Review and test generated security configuration before use, especially CSRF settings and public route rules.

Risk: The skill can propose file edits and shell commands in a project.

Mitigation: Review proposed changes and commands before execution, then run project tests and security checks before deployment.

Risk: The included validator is a convenience check rather than a strict release gate.

Mitigation: Pair validator results with normal code review, automated tests, and application security review.

## Reference(s):

- [Java Spring Boot Guide](references/GUIDE.md)
- [Java Spring Boot Patterns](references/PATTERNS.md)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)
- [ClawHub Skill Page](https://clawhub.ai/watermelon11/skills/java-spring-boot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Java, YAML, properties, and shell snippets for Spring Boot development workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and assets/config.yaml; SKILL.md frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
