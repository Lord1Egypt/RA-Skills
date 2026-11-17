## Description:

Use the unofficial go-exa client for web search, page contents, cited answers, agent runs and Websets in Go. Applies when adding Exa integration or working with an existing github.com/psyb0t/go-exa import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add the unofficial go-exa client to a project and write integrations for Exa search, page contents, cited answers, agent runs, and Websets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, page URLs, and answer prompts are sent to Exa and may expose private information.

Mitigation: Keep secrets and private data out of requests.

Risk: API calls can incur charges, and agent runs may run longer and cost more.

Mitigation: Consider endpoint costs and start agent runs only when requested.

Risk: The client is unofficial, and its implementation was outside the verified artifact.

Mitigation: Review and pin the dependency before building.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-exa project repository](https://github.com/psyb0t/go-exa)
- [go-exa package documentation](https://pkg.go.dev/github.com/psyb0t/go-exa)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
