## Description:

Writes Go code with go-contextual-ai (package contextual, github.com/psyb0t/go-contextual-ai), an unofficial client for the Contextual AI API generated with oapi-codegen. `contextual.NewClientWithResponses(baseURL, opts...)` gives a typed method for every endpoint in Contextual AI's OpenAPI spec (agents, agent queries, datastores, documents, extraction, generate, LMUnit, parse jobs, rerank, billing, users), with request structs and decoded `JSON200`/`JSON422` response fields. Auth is a bearer API key added through a request editor. Use when Go code needs to call the Contextual AI API, or already imports go-contextual-ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to write Go code that integrates with Contextual AI, including querying agents and managing related resources. It provides installation, authentication, endpoint lookup, and typed response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the client sends requests and supplied data to the configured Contextual AI API base URL.

Mitigation: Confirm the destination and data are appropriate, and keep the bearer API key in an environment variable rather than committing or logging it.

Risk: The security assessment was partial because one local reference could not be resolved.

Mitigation: Review the skill's references and behavior before relying on the assessment.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-contextual-ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may include API request code and typed response handling.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
