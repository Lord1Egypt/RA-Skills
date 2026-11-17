## Description:

Read and manage a My Hot Lunchbox school-lunch account from a shell with curl — sign in, list students, read the lunch calendar and cart, check orders, deliveries and payments. Use when you want My Hot Lunchbox data without running the MCP server, in a script, or on a machine where the MCP is not installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents can use the shell commands to read and manage a My Hot Lunchbox school-lunch account, including its students, calendar, cart, orders, and payments. It is intended for scripts or environments where the MCP server is not installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell skill can create or change orders and can start checkout that charges a real card, beyond reading account data.

Mitigation: Inspect write payloads, confirm the returned checkout total before paying, and do not call checkout speculatively.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/myhotlunchbox-mcp)
- [My Hot Lunchbox endpoints](references/endpoints.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON data, PDF reports, Guidance]

**Output Format:** [Markdown instructions with shell code blocks; API responses are typically JSON and printable reports are PDF]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires My Hot Lunchbox account credentials; returned account data varies by user.]

## Skill Version(s):

1.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
