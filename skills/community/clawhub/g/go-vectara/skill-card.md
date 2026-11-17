## Description:

An unofficial, typed Go client for Vectara API v2 that supports corpora, documents, search, RAG queries, chats, agents, tools, pipelines, and account administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate applications with Vectara API v2 for corpus and document operations, search and RAG queries, and chats, agents, tools, and pipelines. It is also useful when working in a project that already imports github.com/psyb0t/go-vectara.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign but partial, with medium confidence; two local references could not be resolved.

Mitigation: Review the unresolved references and check relevant operations before use.

Risk: Creating, updating, deleting, or resetting resources changes account data; queries and agent execution may consume account resources or invoke configured tools.

Mitigation: Run account-changing operations only when requested, confirm the intended account and operation, and keep credentials in environment variables rather than source code.

## Reference(s):

- [Setup and reference guide](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-vectara)
- [Project homepage](https://github.com/psyb0t/go-vectara)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential setup using environment variables; generated code can create or modify Vectara account resources.]

## Skill Version(s):

0.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
