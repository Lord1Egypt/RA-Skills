## Description:

Manage Omnium Hub CRM (contacts, opportunities, appointments). Use for all CRM-related tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omniumhub](https://clawhub.ai/user/omniumhub)

### License/Terms of Use:


## Use Case:

CRM operators and agents use this skill to look up, create, and update contacts and to list or create CRM opportunities through Omnium Hub workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a live Omnium Hub API key and may expose it through command-line usage.

Mitigation: Use a narrowly scoped, revocable API key and prefer protected storage or environment variables for secret handling.

Risk: The skill can send or change CRM contact and opportunity data through LeadConnectorHQ services.

Mitigation: Install only after confirming LeadConnectorHQ is the intended Omnium Hub API provider and reviewing the supported actions and external host.

Risk: CRM contact and opportunity data may be printed in command output or logs.

Mitigation: Avoid running the skill where command output is broadly logged, and review output handling before processing sensitive CRM records.

## Reference(s):

- [Omnium Hub CRM skill page](https://clawhub.ai/omniumhub/skills/omnium-hub-crm)
- [LeadConnectorHQ services endpoint](https://services.leadconnectorhq.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses from the CRM client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Omnium Hub API key and command parameters for the selected contacts or opportunities action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
