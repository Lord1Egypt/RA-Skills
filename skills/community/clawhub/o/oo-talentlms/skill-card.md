## Description:

Operate TalentLMS to read and manage users, courses, groups, categories, and branches through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

TalentLMS administrators and operators can inspect users, courses, groups, categories, and branches, and create, update, or delete user records through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute a downloaded installer without verification or clear user approval.

Mitigation: Review and approve CLI setup separately, including installation and synchronization of other agent skills. Prefer a reviewed, version-pinned installation.

Risk: The connected account can change or delete TalentLMS records.

Mitigation: Retain the skill's required confirmations before changing or deleting records.

## Reference(s):

- [TalentLMS](https://www.talentlms.com)
- [TalentLMS API documentation](https://developers.talentlms.io/intro)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON requests and responses with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation; deletion requires explicit approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
