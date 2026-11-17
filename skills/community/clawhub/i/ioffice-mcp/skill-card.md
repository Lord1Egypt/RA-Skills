## Description:

Access iOffice workspace and facility data via MCP for buildings, floors, spaces, reservations, visitors, maintenance requests, moves, and mail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill with their employer-authorized iOffice tenant to look up workplace information and manage bookings, visitors, maintenance requests, moves, and mail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separately installed ioffice-mcp server and its confirmation enforcement were not verified.

Mitigation: Use an employer-approved server version and least-privilege credentials, protect its configuration, and review each confirmation before changes or deletions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chrischall/skills/ioffice-mcp)
- [npm package](https://www.npmjs.com/package/ioffice-mcp)
- [Project repository (linked in the skill documentation)](https://github.com/chrischall/ioffice-mcp)

## Skill Output:

**Output Type(s):** [Text, JSON data, API actions]

**Output Format:** [Natural-language responses, iOffice records, and operation receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results may be compact or full; reservation and mail lists also support brief summaries.]

## Skill Version(s):

3.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
