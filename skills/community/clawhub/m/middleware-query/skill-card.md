## Description:

Natural-language read-only querying for MySQL, Redis, and MongoDB with explicit connection configuration, guarded query planning, and deterministic script executors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gakkiismywife](https://clawhub.ai/user/gakkiismywife)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query local MySQL, Redis, and MongoDB data sources in natural language while routing requests through read-only query plans and guarded executors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles database credentials and can access sensitive database contents.

Mitigation: Use least-privileged read-only database accounts, keep real credentials outside the skill directory unless protected and gitignored, and require TLS for remote database hosts.

Risk: Natural-language query text may be sent to an external LLM when OPENAI_API_KEY is configured.

Mitigation: Disable OPENAI_API_KEY unless sending query text and schema hints to the external LLM provider is acceptable.

Risk: Database reads may expose regulated or personal data in previews.

Mitigation: Prefer local or private test databases, enforce result limits, and review outputs before sharing them.

## Reference(s):

- [Configuration](references/config.md)
- [Examples](references/examples.md)
- [Plan Schema](references/plan-schema.json)
- [Safety Policy](references/safety-policy.md)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON query results and concise Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include datasource/profile used, sanitized operation, count, truncated preview, and a short interpretation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
