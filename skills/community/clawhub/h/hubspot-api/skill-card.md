## Description:

Guides agents through HubSpot CRM searches, record management, and approved automations using a Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

CRM users and developers use this skill to find and manage HubSpot contacts, companies, deals, associations, and properties, and to configure user-approved CRM automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected account may grant access beyond the CRM endpoints documented by the skill.

Mitigation: Grant only the OAuth scopes needed for the task and ask before accessing other endpoints.

Risk: Writes, deletions, and bulk operations can change or remove live CRM records.

Mitigation: Prefer read-only calls and confirm the target and effect before each write, deletion, or bulk operation.

Risk: Triggers and destinations can keep forwarding future CRM events until removed.

Mitigation: Require separate explicit approval for event forwarding and review the destination and ongoing scope.

## Reference(s):

- [HubSpot skill release](https://clawhub.ai/byungkyu/skills/hubspot-api)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [HubSpot API overview](https://developers.hubspot.com/docs/api/overview)
- [HubSpot trigger reference](references/hubspot/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with inline commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CRM operations and automations require an authorized HubSpot connection.]

## Skill Version(s):

1.2.9 (source: ClawHub release metadata; skill frontmatter says 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
