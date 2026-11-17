## Description:

Lint and validate Helm charts for structure, security, dependencies, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to check Helm chart directories for structural issues, security heuristics, dependency consistency, and chart best practices before publishing or deploying charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security results are heuristic and may miss issues or report findings that require reviewer judgment.

Mitigation: Treat linter output as advisory and keep human review or established chart security checks in the release process.

Risk: Reports may include snippets from values.yaml, including possible secret-like values.

Mitigation: Review generated reports before sharing or publishing them when chart values may contain real secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/helm-chart-linter)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown guidance with shell commands and optional text, JSON, or Markdown linter reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled linter exits 0 for no issues, 1 for findings or strict-mode warnings, and 2 for usage errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
