## Description:

API testing and monitoring skill. Test REST and GraphQL APIs, validate responses, and monitor uptime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test REST and GraphQL endpoints, validate API responses, run API test suites, and monitor endpoint uptime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tests may send headers, request bodies, GraphQL queries, validation data, tokens, internal URLs, or sensitive payloads to user-selected endpoints.

Mitigation: Use test credentials and non-sensitive payloads, confirm endpoint destinations before running tests, and avoid including secrets or internal URLs unless they are intentionally part of the test.

Risk: The referenced helper script is not packaged in the artifact, so commands shown by the skill may require additional local tooling before they can run.

Mitigation: Verify the required helper script or equivalent API testing tool exists in the execution environment before relying on generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-api-tester)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include endpoint URLs, request headers, bodies, GraphQL queries, validation schemas, monitoring intervals, and expected response assertions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
