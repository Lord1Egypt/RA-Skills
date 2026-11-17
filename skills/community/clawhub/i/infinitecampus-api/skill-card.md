## Description:

Query an Infinite Campus (Campus Parent portal) district directly with curl instead of running the infinitecampus-mcp server — log in with a real username/password, capture the session cookie + XSRF token, and curl grades, attendance, assignments, schedule, messages, documents, and fees. Use when you want IC data without the MCP, in a script, or on a machine where the MCP isn't installed. Infinite Campus is per-district: the base URL and district app name are configurable, not hardcoded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and developers can use these shell recipes to sign in to their district's Infinite Campus portal and retrieve student grades, attendance, assignments, schedules, messages, documents, and fees without installing the MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that student behavior and food-service records may be accessible even though those data categories are not clearly disclosed in the stated purpose.

Mitigation: Confirm the district enables and intends these data categories before querying them, and omit behavior or food-service requests when they are not needed.

Risk: The login flow uses a real portal password and stores session cookies and an XSRF token for subsequent requests.

Mitigation: Keep credentials in a secret store, restrict access to the temporary cookie jar, and remove the jar when the session is finished.

Risk: Retrieving an individual message body may mark it as read on some district configurations.

Mitigation: Account for this possible read-state change before fetching message bodies.

## Reference(s):

- [Endpoint recipes](references/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/infinitecampus-api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON data]

**Output Format:** [Markdown guidance with curl and jq examples; the queried portal returns JSON or HTML data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [District-specific portal URL and app name; includes login and session-cookie handling guidance.]

## Skill Version(s):

3.3.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
