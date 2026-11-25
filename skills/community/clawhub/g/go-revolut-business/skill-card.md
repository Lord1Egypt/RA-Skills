## Description:

Unofficial Go client for the Revolut Business REST API, generated with oapi-codegen. Package revolut (github.com/psyb0t/go-revolut-business) has revolut.NewClientWithResponses, which returns a client with one typed method per endpoint (accounts, transactions, counterparties, payments, transfers and more). Auth is a bearer access token set through revolut.WithRequestEditorFn, and responses decode into JSON200, JSON201 and JSONDefault fields. Use when Go code needs to call the Revolut Business API or already imports go-revolut-business.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add and call the Revolut Business API client from Go projects, including reading account data and constructing supported operations such as payments and transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because one reference could not be resolved, so its benign verdict does not guarantee zero risk.

Mitigation: Review the setup and authentication guidance before use and develop against the Revolut sandbox.

Risk: Payment, transfer, exchange, and delete operations can move money or remove data.

Mitigation: Use the sandbox while developing and call these operations only when the user has requested the action.

Risk: A bearer access token can expose access to Revolut Business data and operations if disclosed.

Mitigation: Read the token from an environment variable; do not hardcode, commit, log, or print request headers.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-revolut-business)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
