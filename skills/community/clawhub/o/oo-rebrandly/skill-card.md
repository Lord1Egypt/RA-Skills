## Description:

Rebrandly (rebrandly.com). Use this skill for ANY Rebrandly request — reading, creating, updating, and deleting data. Whenever a task involves Rebrandly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read and manage Rebrandly account data through their connected account. It supports link and domain lookup, link creation and updates, and link deletion, with approval required for state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote CLI installer whose release and hosted runtime are unverified.

Mitigation: Review and approve the CLI installation separately, preferably using a verified release, before using the skill.

Risk: Setup may install additional agent skills and the connected account may grant OOMOL access to Rebrandly data.

Mitigation: Review the additional skills and the account permissions granted to OOMOL before connecting the account.

## Reference(s):

- [Rebrandly API documentation](https://developers.rebrandly.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Rebrandly homepage](https://www.rebrandly.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results may include execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
