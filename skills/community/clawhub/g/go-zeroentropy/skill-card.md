## Description:

Provides Go developers with a typed, unofficial client and usage guidance for ZeroEntropy retrieval, reranking, embeddings, indexing, and account operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to add the ZeroEntropy client to a Go project for search, reranking, embeddings, indexing, and account administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provider announced product retirement after September 4, 2026, so service availability may be limited.

Mitigation: Check the linked sunset notice and confirm current availability before adopting the integration; plan an alternative if needed.

Risk: API keys and document download tokens are credentials; account changes can affect data, and queries or model calls can incur charges.

Mitigation: Protect credentials, avoid logging tokenized URLs, send only authorized data, and review account changes and usage costs before making calls.

## Reference(s):

- [Setup and API usage reference](artifact/references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-zeroentropy)
- [ZeroEntropy dashboard](https://dashboard.zeroentropy.dev/)
- [ZeroEntropy sunset notice](https://www.zeroentropy.dev/articles/zeroentropy-is-joining-notion/)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
