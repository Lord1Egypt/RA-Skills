## Description:

Unofficial Go client for the Latitude LLM ops platform API at latitude.so (not Latitude.sh), generated with oapi-codegen. Package latitude (github.com/psyb0t/go-latitude-llm) provides latitude.NewClientWithResponses with a typed ...WithResponse method for every endpoint: projects, traces and spans, scores and annotations, saved searches, issues, API keys, OAuth keys, account and members. Auth is an organization API key or user OAuth token as a Bearer header added through a request editor. Use when Go code needs to call the Latitude LLM API, or already imports go-latitude-llm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers writing Go applications use this skill to install and call the unofficial Latitude LLM API client to inspect projects, traces, scores and issues, or perform authorized organization operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials can expose private traces and enable organization changes.

Mitigation: Use appropriately scoped credentials, keep credentials and trace contents out of logs, and make changes only within the user's request.

Risk: Deletion and export actions can affect organization data or send export links by email.

Mitigation: Confirm deletions and export recipients before proceeding.

Risk: The external Go dependency's implementation was not verified in the release review.

Mitigation: Review and pin the dependency before use.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-latitude-llm)
- [Project homepage](https://github.com/psyb0t/go-latitude-llm)
- [Latitude API endpoint](https://api.latitude.so)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-latitude-llm)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usage examples and instructions for authentication, requests, and responses.]

## Skill Version(s):

0.1.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
