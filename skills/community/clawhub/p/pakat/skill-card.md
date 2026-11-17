## Description:

Interact with the Pakat email marketing API to manage mailing lists, subscribers, campaigns, templates, transactional emails, segments, campaign statistics, and delivery logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hadifarnoud](https://clawhub.ai/user/hadifarnoud)

### License/Terms of Use:


## Use Case:

External users, developers, and marketing operators use this skill to have an agent prepare Pakat REST API requests for email-list administration, subscriber operations, campaign work, transactional email sending, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate requests that send real email or modify and delete Pakat mailing-list data.

Mitigation: Require a preview and explicit confirmation before sends, deletes, imports, unsubscribes, and list changes.

Risk: A Pakat API key can allow account actions through the live API.

Mitigation: Use the least-privileged API key available and store it only in the PAKAT_API_KEY environment variable.

Risk: Subscriber records, tracking data, and delivery logs may contain personal or consent-sensitive information.

Mitigation: Handle subscriber and tracking data according to applicable privacy, consent, and retention obligations.

Risk: Unsafe shell encoding of user-provided HTML can introduce command-injection risk.

Mitigation: Use heredocs or temporary files for base64 encoding and avoid echo with unsanitized input.

## Reference(s):

- [Pakat API Reference](references/api_reference.md)
- [Pakat OpenAPI Specification](references/openapi.json)
- [Pakat API Key Management](https://new.pakat.net/customer/api-keys/index)
- [Pakat Platform](https://pakat.net)
- [Pakat API Base URL](https://new.pakat.net/api)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline curl commands and REST API parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and PAKAT_API_KEY; generated commands may operate on live Pakat account data if executed.]

## Skill Version(s):

1.1.2 (source: server release metadata, created 2026-02-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
