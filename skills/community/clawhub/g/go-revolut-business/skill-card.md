## Description:

Unofficial Go client for the Revolut Business REST API, generated with oapi-codegen. Package revolut (github.com/psyb0t/go-revolut-business) has revolut.NewClientWithResponses, which returns a client with one typed method per endpoint (accounts, transactions, counterparties, payments, transfers and more). Auth is a bearer access token set through revolut.WithRequestEditorFn, and responses decode into JSON200, JSON201 and JSONDefault fields. Use when Go code needs to call the Revolut Business API or already imports go-revolut-business.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate Go applications with the Revolut Business API, including reading business data and implementing payment, transfer, exchange, or deletion operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment, transfer, exchange, and delete operations can move funds or remove data.

Mitigation: Prefer the sandbox while developing and call these operations only when the user requested that action.

Risk: A bearer access token can expose API access if it is hardcoded, committed, logged, or printed.

Mitigation: Read the token from a protected environment variable; do not commit or log it, and do not print request headers.

Risk: The security scan is benign with medium confidence but partial because one reference could not be resolved.

Mitigation: Review the unresolved reference and treat the scan as one input before installing.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-revolut-business source repository](https://github.com/psyb0t/go-revolut-business)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-revolut-business)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and guidance for using the typed Go client; no files are produced by the library itself.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
