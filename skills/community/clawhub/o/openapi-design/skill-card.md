## Description:

API design specification and best practices skill for designing APIs, reviewing existing APIs, generating API documentation, and standardizing interface specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sydpz](https://clawhub.ai/user/sydpz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design REST APIs, review existing API designs, generate OpenAPI documentation, and standardize endpoint, naming, error, security, and versioning practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation examples include unpinned external CLI, Docker, GitHub Actions, and remote ruleset references if users choose to run them.

Mitigation: Pin npm package versions, Docker image digests, GitHub Action commits, and remote rulesets; prefer project-local dependencies over global installs.

Risk: Example tokens, passwords, URLs, and user data could be mistaken for production values.

Mitigation: Treat all tokens, passwords, URLs, and user data in examples as placeholders.

## Reference(s):

- [API Design Principles](references/common/design-principles.md)
- [Naming Conventions](references/common/naming-conventions.md)
- [HTTP Status Codes](references/common/http-status-codes.md)
- [Error Response Format](references/common/error-response-format.md)
- [API Versioning Strategy](references/common/versioning-strategy.md)
- [Resource Modeling](references/design/resource-modeling.md)
- [Endpoint Design](references/design/endpoint-design.md)
- [Security Best Practices](references/design/security-best-practices.md)
- [Documentation Generation Guide](references/documentation/doc-generation-guide.md)
- [API Review Checklist](references/review/api-review-checklist.md)
- [OpenAPI 3.0 Template](references/templates/openapi3-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with OpenAPI YAML and JSON examples, review checklists, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API review reports, OpenAPI templates, documentation outlines, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
