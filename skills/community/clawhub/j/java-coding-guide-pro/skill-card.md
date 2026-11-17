## Description:

Provides Chinese-language Java coding standards and review guidance for Java and Spring Boot code, covering null safety, collections, dates, IO, HTTP, JSON, concurrency, object mapping, crypto, logging, money calculations, modern Java feature gating, and conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baixuanzhu](https://clawhub.ai/user/baixuanzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to generate, modify, refactor, and review Java/Spring Boot code according to opinionated Java coding standards and project-stack adaptation rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate broadly on Java/Spring work and propose changes beyond the immediate request.

Mitigation: Review generated code and dependency changes before applying them, and keep project-specific stack and JDK constraints as the deciding authority.

Risk: Crypto examples or guidance may be incomplete for production security contexts.

Mitigation: Do not copy crypto snippets directly into production; require authenticated encryption, proper key management, and security review.

Risk: Date and time examples may rely on locale or time zone assumptions.

Mitigation: Choose explicit project-approved ZoneId or Clock values instead of copying examples blindly.

## Reference(s):

- [Null Safety and Strings](references/01-null-and-string.md)
- [Collections and Stream](references/02-collection-stream.md)
- [Date and Time](references/03-date-time.md)
- [File IO, HTTP, and JSON](references/04-io-http-json.md)
- [Concurrency](references/05-concurrency.md)
- [Object Mapping and Beans](references/06-object-mapping.md)
- [Crypto](references/07-crypto.md)
- [Exceptions and Logging](references/08-exception-logging.md)
- [Modern Java](references/09-modern-java.md)
- [BigDecimal and Money](references/10-bigdecimal.md)
- [Java Conventions](references/11-conventions.md)
- [Complexity](references/12-complexity.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Java code examples and dependency snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; follows detected project JDK and existing Java stack.]

## Skill Version(s):

1.0.0 (source: server release metadata; source skill frontmatter reports 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
