## Description:

Operate Agenty through an OOMOL-connected account to manage data and run Agenty actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Agenty agents, jobs, and lists, and to retrieve page content, exports, and files through a connected Agenty account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloads that were unavailable for inspection and add agent skills without clearly disclosing those changes.

Mitigation: Review the selected installer and release before setup, and inspect the CLI's skill synchronization behavior. Use OO_SKILLS_SYNC_DISABLED to disable startup synchronization when appropriate.

Risk: Agenty access is mediated through OOMOL, which injects credentials server-side.

Mitigation: Review the OOMOL connection and its granted access before using the skill.

## Reference(s):

- [Agenty API documentation](https://agenty.com/docs/api)
- [Agenty](https://agenty.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Guidance]

**Output Format:** [Agenty action results as JSON or text, with downloadable files where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data and file formats depend on the selected Agenty action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
