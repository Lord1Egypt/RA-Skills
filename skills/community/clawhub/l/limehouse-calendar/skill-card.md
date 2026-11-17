## Description:

Read and write calendar events with granular per-calendar permissions. Users control which calendars an agent can access and whether it can read, create, update, or delete events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madeleinenakada](https://clawhub.ai/user/madeleinenakada)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent authenticate to Limehouse Calendar and manage calendar events subject to per-calendar permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses credentialed access to calendar data through CAL_API_KEY and returned agent_token values.

Mitigation: Treat tokens like passwords, store them only in approved secret storage, and grant the narrowest calendar permissions needed.

Risk: Calendar access can include event deletion when can_delete is granted.

Mitigation: Avoid granting delete access unless required and confirm event details before any delete operation.

Risk: Using the skill shares authorized calendar data with cal.limehouse.io.

Mitigation: Install only when the user trusts Limehouse Calendar with the calendar data made available to the agent.

## Reference(s):

- [Limehouse Calendar ClawHub listing](https://clawhub.ai/madeleinenakada/skills/limehouse-calendar)
- [Limehouse Calendar API base endpoint](https://cal.limehouse.io/api/v1)
- [Limehouse Calendar setup flow](https://cal.limehouse.io/connect)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with HTTP endpoint examples, JSON schemas, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAL_API_KEY and curl; API responses are JSON from the Limehouse Calendar service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
