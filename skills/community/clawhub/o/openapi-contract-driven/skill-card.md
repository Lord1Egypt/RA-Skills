## Description:

OpenAPI Contract Driven guides multi-agent development teams to use an OpenAPI YAML contract, generated TypeScript API clients, CI checks, and role-specific agent rules to keep frontend and backend API work aligned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmpanda011172](https://clawhub.ai/user/kmpanda011172)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to standardize REST API collaboration across human and agent contributors, especially when frontend and backend work frequently diverge. It provides OpenAPI templates, validation scripts, generated client patterns, CI checks, migration guidance, and role-specific agent instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included OpenAPI-to-TypeScript generator can embed untrusted API-spec text into executable frontend code.

Mitigation: Treat OpenAPI YAML changes like source code, require review before generation, and harden or replace generate-api-client.sh before using generated clients in production.

Risk: Repositories that accept OpenAPI specs from pull requests, shared contract repos, vendors, or other semi-trusted sources have elevated review needs.

Mitigation: Review the skill before installation in those repositories and require trusted maintainers to approve changes to specs, generated clients, and CI workflow files.

Risk: Unpinned npm dependencies or CI actions can change behavior after the skill is adopted.

Mitigation: Pin the npm dependency and CI actions before relying on this workflow for production release gates.

## Reference(s):

- [OpenAPI template](references/openapi-template.yaml)
- [API rules checker](references/check-api-rules.sh)
- [API client generator](references/generate-api-client.sh)
- [GitHub Actions contract check](references/ci-github-actions.yml)
- [Migration guide](references/migration-guide.md)
- [Zalando REST API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)
- [Azure API Style Guide](https://github.com/Azure/azure-api-style-guide)
- [OpenAPI 3.0.3 Specification](https://spec.openapis.org/oas/v3.0.3)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, YAML configuration, and TypeScript code/templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable OpenAPI templates, role-specific agent rule snippets, migration guidance, CI workflow configuration, and API client generation scripts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
