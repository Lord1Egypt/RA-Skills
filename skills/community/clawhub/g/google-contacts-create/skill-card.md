## Description:

Creates a new Google contact and retries internally until the operation succeeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to create a Google contact through Composio-backed Google access from structured input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a user's Google Contacts account by creating a contact.

Mitigation: Use it only with intended Composio-backed Google access, apply least-privileged credentials where possible, and confirm contact details before invocation.

Risk: A retried or partially successful run may create duplicate contacts.

Mitigation: Check for duplicate contacts after retries or partial failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-contacts-create)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [JSON object representing the result of the contact creation operation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and COMPOSIO_API_KEY environment variable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
