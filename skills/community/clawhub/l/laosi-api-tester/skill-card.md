## Description:

API Tester Pro helps agents construct and send HTTP, REST, and GraphQL requests, validate status codes, headers, response bodies, and latency, and summarize benchmark results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to exercise APIs after deployment, generate request examples, check service health, validate API contracts, and compare basic latency measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-directed HTTP requests from the agent environment to arbitrary URLs, including sensitive internal or cloud-metadata addresses.

Mitigation: Use it only with trusted endpoints and apply host or network controls that block internal, loopback, link-local, and cloud-metadata ranges when appropriate.

Risk: The implementation saves tested URLs and request history to api_tests.json, which may expose sensitive endpoints or query parameters.

Mitigation: Avoid placing secrets in URLs, prefer protected headers for credentials, and remove or protect api_tests.json after testing sensitive systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-api-tester)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code blocks, request examples, validation rules, and structured result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled implementation may create api_tests.json containing tested URLs, status values, latency, errors, and timestamps.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
