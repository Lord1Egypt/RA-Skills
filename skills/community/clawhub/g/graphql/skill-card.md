## Description:

Designs, debugs, and hardens GraphQL schemas, resolvers, and clients, including N+1 batching, nullability, cost limits, subscriptions, federation, cache behavior, schema evolution, and production security posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, review, debug, secure, test, and evolve GraphQL APIs across schemas, resolvers, clients, federation boundaries, subscriptions, and production deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse prior GraphQL project details from local preference memory.

Mitigation: Review ~/Clawic/data/graphql/ before use if prior project context should not influence new guidance.

Risk: The documentation includes optional npx and CLI examples that may install or execute local tooling.

Mitigation: Pin or locally install the referenced GraphQL CLI tools before running command examples.

Risk: Generated API guidance may be incomplete or inappropriate for a specific production threat model.

Mitigation: Review proposed schemas, resolver logic, authorization checks, cost limits, and transport controls before deployment.

## Reference(s):

- [ClawHub GraphQL Skill Page](https://clawhub.ai/ivangdavila/skills/graphql)
- [Clawic GraphQL Skill Homepage](https://clawic.com/skills/graphql)
- [Setup Guide](artifact/setup.md)
- [Security Guide](artifact/security.md)
- [Commands Toolkit](artifact/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with GraphQL, JSON, YAML, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and apply user preferences from ~/Clawic/data/graphql/ when present; otherwise uses documented defaults.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
