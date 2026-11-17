## Description:

Use a connected Pipedrive account to read and search CRM records and create, update, or delete activities, deals, organizations, and people.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Pipedrive users and teams can use this skill to manage CRM records through their connected account, including looking up existing information and making requested changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may run downloaded software from the internet without independent verification.

Mitigation: Review and independently verify the CLI installer before running it; avoid executing a downloaded script unchecked.

Risk: Connecting Pipedrive entrusts OOMOL with credential handling and access to business data; the skill can also change or delete records.

Mitigation: Review the account access being granted, confirm the exact payload and effect before writes, and get explicit approval for the target before deletion.

## Reference(s):

- [Pipedrive skill page](https://clawhub.ai/oomol/skills/oo-pipedrive)
- [Pipedrive](https://www.pipedrive.com)
- [Pipedrive API documentation](https://developers.pipedrive.com/docs/api/v1)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text]

**Output Format:** [Structured Pipedrive record data and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data varies by action; write actions require confirmation and deletions require explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
