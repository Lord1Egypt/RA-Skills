## Description:

Operate Freshsales through a connected account to read and manage contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams use this skill to read Freshsales contacts and to create, update, or delete contacts through their connected account. The skill requires approval for changes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup instructions run a downloaded CLI installer without a separate approval step, and the installer and CLI were not verified in the supplied security review.

Mitigation: Review and approve the CLI installation separately, including any changes it makes to other installed agent skills.

Risk: Connecting Freshsales authorizes OOMOL to mediate access to CRM data, while create, update, and delete actions can change records.

Mitigation: Review the requested access and keep the skill's user approval requirement for every write or deletion.

## Reference(s):

- [Freshsales CRM](https://www.freshworks.com/crm/sales/)
- [Freshworks CRM API documentation](https://developers.freshworks.com/crm/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changes and deletions require user approval.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
