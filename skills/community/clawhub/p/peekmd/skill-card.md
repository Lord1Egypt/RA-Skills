## Description:

Peekmd helps agents, bots, and developers create shareable rendered markdown web pages through the peekmd.dev API with optional expiration and deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notacryptodad](https://clawhub.ai/user/notacryptodad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Peekmd to turn markdown reports, documents, code snippets, tables, and diagrams into temporary or shareable web pages for agent-to-human handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected markdown is sent to peekmd.dev and may be exposed through a shareable URL.

Mitigation: Review and redact secrets, credentials, personal data, regulated content, internal reports, and private logs before creating a page.

Risk: Shared pages can remain accessible until their TTL expires or they are deleted.

Mitigation: Use short TTL values for temporary shares and call the burn endpoint when a page should be removed immediately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/notacryptodad/skills/peekmd)
- [Peekmd homepage](https://peekmd.dev)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces shareable URLs for rendered markdown pages; free-tier pages expire after five minutes and submitted markdown is limited to 500 KB.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
