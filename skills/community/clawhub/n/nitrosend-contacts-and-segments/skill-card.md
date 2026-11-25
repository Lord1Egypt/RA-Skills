## Description:

Manage contacts, email lists, segments, tags and subscribers: import contacts by CSV, sync HubSpot or Attio, search a contact's history, build segments from data and engagement, and verify email addresses to clean the list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email audience managers use this skill to find and organize contacts, maintain lists and tags, build engagement-based segments, and validate addresses. It supports audience management and email list hygiene through Nitrosend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding contacts to a list can trigger live flows.

Mitigation: Review the target list and intended recipients before adding contacts.

Risk: Importing contacts without authorization can result in emailing people who have not been approved to receive messages.

Mitigation: Import only contacts the user is authorized to email.

Risk: Deleting contacts or lists can remove audience data.

Mitigation: Preview the deletion and obtain the user's confirmation before deleting.

## Reference(s):

- [Managing contacts](https://docs.nitrosend.com/guides/managing-contacts)
- [Segments](https://docs.nitrosend.com/concepts/segments)

## Skill Output:

**Output Type(s):** [Text, Structured audience data, Guidance]

**Output Format:** [Text responses with contact, list, segment, or validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contact and audience details returned by Nitrosend.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
