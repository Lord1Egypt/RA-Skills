## Description:

OAuth proxy for calling external APIs (Oura, Google Calendar, etc.) via Perpetua.sh hosted API using a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielkillenberger](https://clawhub.ai/user/danielkillenberger)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure and call the Perpetua.sh hosted OAuth proxy for Oura data, Google Calendar events, and OAuth connection management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Oura health data and Google Calendar data may be sensitive when routed through the third-party Perpetua.sh proxy.

Mitigation: Install only when this proxy is intended, review OAuth scopes during account connection, and limit requests to data needed for the task.

Risk: The PERPETUA_API_KEY grants access to connected provider data through the hosted API.

Mitigation: Store PERPETUA_API_KEY in a secret manager or protected environment file and avoid exposing it in logs, prompts, or shared shell history.

## Reference(s):

- [Perpetua.sh API](https://www.perpetua.sh/api)
- [ClawHub Skill Page](https://clawhub.ai/danielkillenberger/skills/perpetua)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PERPETUA_API_KEY and the Perpetua.sh hosted API; returned data depends on connected OAuth providers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
