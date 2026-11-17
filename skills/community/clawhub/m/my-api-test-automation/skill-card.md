## Description:

Generate complete automated API test cases from interface documentation such as OpenAPI, Swagger exports, Postman collections, Markdown API docs, or endpoint tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huahuaweiwei](https://clawhub.ai/user/huahuaweiwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to convert API documentation into executable automated test suites, configure environment-specific scripts, run tests when requested, and produce pass/fail reports with coverage gaps and assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run generated API tests against user-provided targets, including requests that change data.

Mitigation: Use non-production targets by default, review generated requests before execution, and confirm production-like environments before sending mutating requests.

Risk: API credentials could be exposed if hard-coded into generated cases or configuration files.

Mitigation: Provide credentials through environment variables or managed secret flows, and keep environment-sensitive values in configuration rather than individual cases.

Risk: Incomplete API documentation can lead to incorrect assumptions or misleading coverage reports.

Mitigation: Record assumptions, blockers, and uncovered cases in the generated report so reviewers can validate coverage before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huahuaweiwei/skills/my-api-test-automation)
- [Environment Contract](references/environment-contract.md)
- [Report Contract](references/report-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated files, JSON configuration, JavaScript assertions, Python scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local API test workspaces, manifests, environment files, scripts, and Markdown or JSON test reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
