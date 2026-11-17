## Description:

Builds and debugs LangChain apps in Python across LCEL chains, agents, tools, retrievers, streaming, structured output, LangGraph workflows, production hardening, testing, observability, security, and migration issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, review, debug, and harden LangChain applications in Python. It is aimed at practical work on chains, agents, retrieval, streaming, structured output, LangGraph state, tests, observability, production limits, security, and version migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local LangChain preferences and project notes may persist across sessions in ~/Clawic/data/langchain/.

Mitigation: Keep secrets and customer data out of those files, and remove the directory if cross-session memory is not desired.

Risk: Generated LangChain guidance and code can be wrong for a specific package version, provider, or deployment environment.

Mitigation: Check the installed lockfile or requirements, run the suggested tests, and review security-sensitive code before use.

Risk: Tracing, retrieved documents, tool arguments, or saved fixtures can expose private data when copied into examples or observability systems.

Mitigation: Redact PII and credentials at the source, avoid storing secrets in metadata or tags, and scrub recorded fixtures before committing them.

## Reference(s):

- [ClawHub LangChain Skill Page](https://clawhub.ai/ivangdavila/skills/langchain)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [Clawic LangChain Skill Homepage](https://clawic.com/skills/langchain)
- [LangChain Skill Guide](artifact/SKILL.md)
- [Setup](artifact/setup.md)
- [Security](artifact/security.md)
- [Production](artifact/production.md)
- [Testing](artifact/testing.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local preferences in ~/Clawic/data/langchain/ when present.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
