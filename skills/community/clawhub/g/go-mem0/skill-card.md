## Description:

Unofficial typed Go client for the Mem0 Platform API, with generated methods for memory, entity, organization, profile, and related operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Go applications with Mem0's hosted memory platform, including memory search and management. It is intended for Go projects that need the Mem0 Platform API rather than Mem0's self-hosted library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory content, queries, and metadata are sent to the Mem0 Platform API.

Mitigation: Send only data intended for Mem0 and scope filters to the relevant user, agent, app, or run.

Risk: Memory and organization operations can change hosted resources, and profile jobs can consume credits.

Mitigation: Limit changes to task-owned resources when requested, confirm the target scope, and account for profile-job charges.

Risk: The API key could be exposed through source code or logs.

Mitigation: Read the key from MEM0_API_KEY; do not hardcode, commit, or log it.

## Reference(s):

- [Setup and API reference](artifact/references/setup.md)
- [go-mem0 source repository](https://github.com/psyb0t/go-mem0)
- [go-mem0 package documentation](https://pkg.go.dev/github.com/psyb0t/go-mem0)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-mem0)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use a Mem0 Platform API key; API requests send memory content, queries, and metadata to Mem0.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
