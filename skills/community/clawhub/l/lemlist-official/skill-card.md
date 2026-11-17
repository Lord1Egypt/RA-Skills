## Description:

Official Lemlist API integration for sales automation and multichannel outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micktaiwan](https://clawhub.ai/user/micktaiwan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent manage Lemlist campaigns, leads, schedules, inbox messages, webhooks, unsubscribes, exports, enrichment, and related account data through the Lemlist API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a Lemlist account and perform powerful account actions, including sending outreach, exporting data, and modifying campaign records.

Mitigation: Install only when account access is intended, use the least-privileged API key available, and require confirmation before sending messages, exporting data, or modifying campaign state.

Risk: Broad unattended instructions could cause unintended outreach, unsubscribe changes, resource deletion, or webhook creation.

Mitigation: Keep agent instructions narrowly scoped and confirm before changing unsubscribes, deleting resources, creating webhooks, or performing other account-changing actions.

## Reference(s):

- [Lemlist API endpoint reference](references/api-endpoints.md)
- [Official Lemlist API documentation](https://developer.lemlist.com/api-reference)
- [ClawHub skill page](https://clawhub.ai/micktaiwan/skills/lemlist-official)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses LEMLIST_API_KEY for authenticated Lemlist API access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
