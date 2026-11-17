## Description:

Builds a sorted index of paths and methods from a user-provided OpenAPI JSON document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

API developers and reviewers use this skill to survey endpoints and prepare smoke-test checklists from an OpenAPI 3 JSON document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A provided local specification may reveal its API surface to the agent session.

Mitigation: Provide only specifications you intend the agent to analyze.

Risk: The endpoint index omits webhooks and callbacks.

Mitigation: Review those sections separately when assessing the full API surface.

## Reference(s):

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [ClawHub skill release](https://clawhub.ai/hmahmadcs/skills/openapi-endpoint-indexer)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text: sorted METHOD path lines and totals by method]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Indexes paths only; excludes webhooks and callbacks.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
