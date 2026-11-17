## Description:

Connects an OOMOL account to Mailchimp for reading and managing audiences, members, tags, and merge fields through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Mailchimp account operators use this skill to inspect audiences and members, and to create, update, archive, or permanently delete member records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supporting CLI may install additional agent skills during startup, and the downloaded installers and hosted connector were not audited, leaving their full effects uncertain.

Mitigation: Review and install the CLI yourself; set OO_SKILLS_SYNC_DISABLED=1 for CLI runs if you do not want automatic skill installation.

Risk: Mailchimp writes and deletions can change or remove account data.

Mitigation: Connect only the intended Mailchimp account and retain the skill's required approvals for changes and deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Mailchimp Marketing API documentation](https://mailchimp.com/developer/marketing/api/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions, oo CLI commands, and JSON Mailchimp responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing and destructive actions require user confirmation; reads can run directly.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
