## Description:

Search, read, and update Pipedrive deals, contacts, organizations, activities, pipelines, and sales workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and CRM users use this skill to find and review Pipedrive records, manage contacts and organizations, and work with deals, activities, and pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating or updating deals, contacts, organizations, activities, or notes changes live CRM records.

Mitigation: Require clear user intent, search and read the target record first, and confirm relevant details before making changes.

Risk: CRM data is accessed through the connected account, and OAuth credentials are stored locally.

Mitigation: Use only the CRM permissions needed, verify the configured API destination belongs to Pipedrive, protect local credentials, and do not send unrelated sensitive content.

## Reference(s):

- [Pipedrive API](https://api.pipedrive.com/api)
- [Pipedrive OAuth token endpoint](https://oauth.pipedrive.com/oauth/token)
- [mcporter](https://github.com/steipete/mcporter)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [API Calls, Structured data, Guidance]

**Output Format:** [Structured CRM data, with optional Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and searches records; create and update actions can change live CRM data.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
