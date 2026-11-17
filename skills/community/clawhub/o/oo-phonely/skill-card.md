## Description:

Search and read Phonely data, including agents, calls, and call transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users with a connected Phonely account can retrieve agent details, call lists, and call summaries or transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified CLI release or allowing automatic skill synchronization could introduce unreviewed changes.

Mitigation: Review and preinstall a verified CLI release, require approval for installation, and consider the documented OO_SKILLS_SYNC_DISABLED control.

Risk: Call transcripts may be accessible through the OOMOL-connected account.

Mitigation: Review whether OOMOL should mediate access to transcripts and use the skill only with appropriately authorized Phonely data.

## Reference(s):

- [Phonely homepage](https://www.phonely.ai/)
- [Phonely API documentation](https://docs.phonely.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON action results with concise text summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval of Phonely agent and call data; available fields depend on the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
