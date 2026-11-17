## Description:

Read appointments, invoices, quotes, and work requests from a Jobber Client Hub using the fpx CLI and a paired browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External Jobber customers can use the skill to inspect service appointments, invoices, quotes, and work requests from shell workflows, including scripts that need structured records without an MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent browser grant provides authenticated access to the approved domain and is broader than a guaranteed read-only permission.

Mitigation: Review the browser grant before pairing; use a narrowly scoped GET-only configuration if available, and revoke pairing when finished.

Risk: The Jobber hub URL is a credential, and saved page HTML may expose private hub data.

Mitigation: Keep hub URLs private; stream HTML to the parser or use private temporary files and delete them afterward.

Risk: The installed CLI and browser extension were outside the artifact audit.

Mitigation: Review the CLI and extension separately before relying on them with an authenticated hub.

## Reference(s):

- [Recipes](references/recipes.md)
- [Why this skill does not use Jobber's documented API](references/why-not-the-api.md)
- [Client Hub parser](references/parse-clienthub.mjs)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured JSON records with shell commands and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records cover one selected page type; returned record URLs are hub-relative.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
