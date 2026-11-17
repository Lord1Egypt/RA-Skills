## Description:

Discover, understand, and query standards-based OData v4.0 or v4.01 services for service-document inspection, metadata review, OData URL construction, entity retrieval, filtering, selecting, expanding, sorting, counting, and server-driven pagination in a read-only workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[try028](https://clawhub.ai/user/try028)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect OData service documents and metadata, compose read-only OData v4 queries, retrieve bounded results, and diagnose response or pagination issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment-provided tokens or headers are sent to configured OData endpoints during queries.

Mitigation: Install only after verifying the saved service roots and profiles point to trusted endpoints.

Risk: Multiple saved profiles or an unexpected default profile can cause queries to target the wrong service.

Mitigation: Review the local profile file and selected default before use, especially in shared or multi-service environments.

Risk: The release package contains stale Python bytecode cache files.

Mitigation: Prefer a repackaged source-only release without __pycache__ files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/try028/skills/odata-query)
- [Configuration](references/configuration.md)
- [Service discovery and capabilities](references/discovery.md)
- [OData v4 query syntax](references/query-syntax.md)
- [Responses, pagination, and errors](references/responses-and-errors.md)
- [Normative OData v4 references](references/standards.md)
- [OData Version 4.01, Part 1: Protocol](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html)
- [OData Version 4.01, Part 2: URL Conventions](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html)
- [OData JSON Format Version 4.01](https://docs.oasis-open.org/odata/odata-json-format/v4.01/os/odata-json-format-v4.01-os.html)
- [OData CSDL XML Representation Version 4.01](https://docs.oasis-open.org/odata/odata-csdl-xml/v4.01/odata-csdl-xml-v4.01.html)
- [OData Version 4.0 standards index](https://docs.oasis-open.org/odata/odata/v4.0/)
- [OData vocabularies](https://github.com/oasis-tcs/odata-vocabularies)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with OData URLs, shell commands, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only GET and discovery requests; profile files store environment-variable names rather than credential values.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
