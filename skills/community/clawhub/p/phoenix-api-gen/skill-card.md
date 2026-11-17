## Description:

Generates Phoenix JSON API code from an OpenAPI specification or natural language description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchapim](https://clawhub.ai/user/gchapim)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scaffold Phoenix REST APIs, including contexts, Ecto schemas, migrations, controllers, JSON renderers, router entries, authentication plugs, tenant scoping, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated multi-tenant authorization patterns may be unsafe if tenant identifiers are accepted from requests without validating authenticated tenant membership.

Mitigation: Review generated security code, validate tenant selection against authenticated membership, scope every read/update/delete by the validated tenant, ignore client-supplied tenant_id on create, and add negative cross-tenant authorization tests.

## Reference(s):

- [Phoenix Conventions Reference](references/phoenix-conventions.md)
- [Ecto Patterns Reference](references/ecto-patterns.md)
- [Test Patterns Reference](references/test-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with generated Elixir, Phoenix, Ecto, router, plug, migration, and ExUnit code blocks or file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Phoenix project files for contexts, schemas, migrations, controllers, JSON renderers, router entries, auth plugs, tests, and factories.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
