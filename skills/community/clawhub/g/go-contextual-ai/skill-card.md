## Description:

Helps Go developers build integrations with Contextual AI using the go-contextual-ai client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go code that calls Contextual AI APIs through the go-contextual-ai client, including agent queries and datastore or document operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client is unofficial and adds a Go dependency.

Mitigation: Review and pin the dependency before use.

Risk: Requests send data to the configured Contextual AI base URL.

Mitigation: Verify the destination and send only data intended for Contextual AI to process.

Risk: Delete, reset, user removal, and ingestion operations can change account data.

Mitigation: Limit these operations to explicitly requested targets.

Risk: API keys can be exposed if embedded in code or logs.

Mitigation: Read the key from an environment variable and do not hardcode, commit, or log it.

## Reference(s):

- [Setup and API usage](references/setup.md)
- [go-contextual-ai on GitHub](https://github.com/psyb0t/go-contextual-ai)
- [go-contextual-ai package documentation](https://pkg.go.dev/github.com/psyb0t/go-contextual-ai)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-contextual-ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may send user-provided content to the configured Contextual AI endpoint.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
