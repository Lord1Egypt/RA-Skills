## Description:

Operate DialMyCalls contacts, groups, and account details through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and assistants with a connected DialMyCalls account can inspect account details and read or manage contacts and groups. The skill provides the relevant action workflows and requires confirmation before changes or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may automatically run downloaded code that has not been verified.

Mitigation: Install a verified oo CLI release manually and prevent automatic installer execution.

Risk: Cross-agent skill synchronization may introduce broader agent changes.

Mitigation: Review or disable synchronization; the upstream setting documented for this is OO_SKILLS_SYNC_DISABLED=1.

Risk: The connected service can expose account and contact data, and some actions change or delete records.

Mitigation: Review the connected account's access and preserve the skill's confirmation requirements for writes and destructive actions.

## Reference(s):

- [DialMyCalls API documentation](https://www.dialmycalls.com/api-documentation)
- [DialMyCalls](https://www.dialmycalls.com)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Text and JSON results with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account, its permissions, and the live action schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
