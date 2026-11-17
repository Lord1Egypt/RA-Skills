## Description:

Identifies contacts you haven't reached out to recently and suggests low-pressure ways to reconnect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and external users use this skill as a local-first personal CRM helper to find overdue contacts and draft lightweight reconnection messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact data is sensitive and can appear in the generated Markdown output.

Mitigation: Install only when comfortable letting the skill read local contacts, keep contacts.json under user control, and avoid sharing generated reports broadly.

Risk: Untrusted contact fields may be rendered as rich Markdown by downstream viewers.

Mitigation: Render generated Markdown in a viewer that disables raw HTML and remote resource loading when possible.

## Reference(s):

- [Personal CRM Warm-Up on ClawHub](https://clawhub.ai/liverock/skills/personal-crm-warm-up)
- [Publisher profile: liverock](https://clawhub.ai/user/liverock)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown report with a summary table and drafted outreach messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output may include contact names, relationship categories, elapsed days, conversation hooks, and suggested messages from the local contacts file.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
