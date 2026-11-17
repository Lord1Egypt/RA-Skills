## Description:

Manage Pipedrive CRM from OpenClaw using API v1, including people, organizations, deals, leads, activities, notes, pipelines, and custom endpoint actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Developers and CRM operators use this skill to manage Pipedrive records through API-backed workflows instead of the Pipedrive UI. It supports contact, organization, deal, lead, activity, note, pipeline, stage, product, and custom endpoint operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, move, or delete live Pipedrive CRM records.

Mitigation: Require manual review before delete, raw request, or bulk update actions, and read the target record before making changes when user intent is ambiguous.

Risk: Pipedrive API credentials may be exposed through shared terminals, recordings, or overly broad permissions.

Mitigation: Use the least-privileged credential available, avoid printing raw tokens, and do not run the setup wizard in shared or recorded terminals.

Risk: A custom PIPEDRIVE_API_BASE can route requests to an unintended destination.

Mitigation: Set PIPEDRIVE_API_BASE only after verifying that the destination is trusted and expected.

## Reference(s):

- [Entity Playbooks](references/entity-playbooks.md)
- [Pipedrive API v1 Notes](references/pipedrive-v1-notes.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pipedrive authentication and company routing environment variables before API calls can run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
