## Description:

Use SimpleTexting to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage SimpleTexting contacts, contact lists, segments, and custom fields through a connected account, including reads and controlled changes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run an online CLI installer without first verifying the release.

Mitigation: Verify the specific CLI release and review the remote installer before allowing installation.

Risk: The CLI mediates access to SimpleTexting account and contact data, and its synchronization settings may affect that access.

Mitigation: Review the CLI's automatic skill synchronization settings and retain the skill's explicit approvals for changes and deletions.

## Reference(s):

- [SimpleTexting](https://simpletexting.com/)
- [SimpleTexting API documentation](https://simpletexting.com/api/docs/v2/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-simpletexting)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Command examples with JSON request and response data, plus concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers read operations and state-changing contact or list actions; documented write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
