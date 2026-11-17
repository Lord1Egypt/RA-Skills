## Description:

Manage Productlane workspace data by reading, creating, updating, and deleting companies and contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use the skill to inspect Productlane companies and contacts, or manage them through a connected Productlane account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloaded software and introduce broader agent changes without clear approval.

Mitigation: Install a verified CLI release separately, require approval before software installation, and disable automatic agent-skill synchronization unless wanted.

Risk: Write and destructive actions can change or remove Productlane workspace records.

Mitigation: Confirm the exact payload for writes and the target and approval for deletions before running them.

## Reference(s):

- [Productlane](https://productlane.com)
- [Productlane API documentation](https://productlane.mintlify.dev/docs/api-v2/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads; action results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
