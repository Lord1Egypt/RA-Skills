## Description:

OData Service helps agents work with OData v4.0 and v4.01 services for model discovery, querying, entity changes, relationships, streams, functions, actions, batch requests, and asynchronous requests with explicit authorization for state-changing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[try028](https://clawhub.ai/user/try028)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure authenticated OData endpoints, inspect service metadata, perform standards-compliant reads and writes, and manage functions, actions, streams, delta tracking, batch, and asynchronous workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes unnecessary Python bytecode in bundled __pycache__ files.

Mitigation: Review or remove the bundled bytecode before installation and rely on the readable source files for inspection.

Risk: The skill can read from and modify configured OData services using environment-provided credentials.

Mitigation: Install only for trusted OData services, configure profiles with environment-variable names rather than secret values, and require explicit confirmation before write, delete, batch, action, or stream update operations.

## Reference(s):

- [OData Service on ClawHub](https://clawhub.ai/try028/skills/odata-service)
- [One-time service configuration](references/configuration.md)
- [Model discovery, addressing, and queries](references/model-and-query.md)
- [Functions, actions, batch, and asynchronous requests](references/operations-batch-async.md)
- [Protocol details, errors, and primary standards](references/protocol-and-errors.md)
- [Streams, media entities, and delta synchronization](references/streams-and-delta.md)
- [Writes, ETags, and relationships](references/writes-and-relationships.md)
- [OData Version 4.01, Part 1: Protocol](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html)
- [OData Version 4.01, Part 2: URL Conventions](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html)
- [OData JSON Format Version 4.01](https://docs.oasis-open.org/odata/odata-json-format/v4.01/os/odata-json-format-v4.01-os.html)
- [OData CSDL XML Version 4.01](https://docs.oasis-open.org/odata/odata-csdl-xml/v4.01/odata-csdl-xml-v4.01.html)
- [OData Version 4.0 standards index](https://docs.oasis-open.org/odata/odata/v4.0/)
- [OASIS OData vocabularies](https://github.com/oasis-tcs/odata-vocabularies)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, shell commands, JSON examples, and request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue guarded HTTP requests to configured OData services through helper scripts when the user authorizes the operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
