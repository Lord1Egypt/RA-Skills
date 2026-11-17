## Description:

Search and read Signalbase data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to search Signalbase company, funding, hiring, acquisition, investor, and job-change data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Signalbase search can trigger an unverified software installer without clear user approval.

Mitigation: Use a reviewed, version-pinned oo CLI; require approval before running installers; review its startup synchronization behavior and disable it with OO_SKILLS_SYNC_DISABLED if needed; confirm that Signalbase access through OOMOL is intended.

## Reference(s):

- [Signalbase homepage](https://www.trysignalbase.com)
- [Signalbase API documentation](https://docs.trysignalbase.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-signalbase)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples; Signalbase results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides search and read actions for Signalbase company and business signal data.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
