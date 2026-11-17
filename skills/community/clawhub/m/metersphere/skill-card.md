## Description:

MeterSphere integrates MeterSphere REST APIs with local scripts so an OpenClaw agent can query testing assets, generate functional and API test cases, import Swagger/OpenAPI definitions, and summarize reviews, defects, and case details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fit2-zhao](https://clawhub.ai/user/fit2-zhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and test teams use this skill to query MeterSphere projects, modules, templates, functional cases, API definitions, API cases, reviews, and defect associations. They can also generate local test-case drafts from requirements or Swagger/OpenAPI inputs and write approved assets back to MeterSphere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security verdict is suspicious because credential-handling and write paths are too unsafe for automatic trust.

Mitigation: Review the skill before deployment, use least-privilege credentials, separate read and write API keys, and test write operations in a non-production MeterSphere environment first.

Risk: The skill sends authenticated requests to a configured MeterSphere base URL and can load OpenAPI inputs from URLs.

Mitigation: Use HTTPS-only trusted MeterSphere URLs, confirm network traffic only reaches the expected base URL, and do not pass untrusted OpenAPI URLs.

Risk: .env files and METERSPHERE_HEADERS_JSON can expose or forward sensitive values.

Mitigation: Tightly control the skill directory and .env file, keep .env limited to expected variables with restrictive permissions, and avoid METERSPHERE_HEADERS_JSON unless it is necessary and reviewed.

Risk: Hardcoded template, version, or project IDs can assign generated assets to the wrong MeterSphere project.

Mitigation: Set METERSPHERE_DEFAULT_TEMPLATE_ID, METERSPHERE_DEFAULT_VERSION_ID, and METERSPHERE_PROJECT_ID explicitly before creation or batch-write workflows.

Risk: Installation verification output can include credential prefixes or environment details.

Mitigation: Avoid sharing raw verification output outside trusted channels and redact credential-related values before support or review handoff.

## Reference(s):

- [MeterSphere API Reference](references/ms-api.md)
- [Functional Case AI Enhancement Prompt](references/ai-functional-case-prompt.md)
- [API Bundle AI Enhancement Prompt](references/ai-api-bundle-prompt.md)
- [Installation Checklist](INSTALLATION_CHECKLIST.md)
- [Signature Algorithm](SIGNATURE_ALGORITHM.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries, JSON payloads, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require MeterSphere credentials, a trusted MeterSphere base URL, python3, openssl, and curl.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
