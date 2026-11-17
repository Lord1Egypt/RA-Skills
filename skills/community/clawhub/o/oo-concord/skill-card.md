## Description:

Concord (concord.app). Use this skill for ANY Concord request — searching and reading data. Whenever a task involves Concord, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Concord users and developers can use the skill to search and read the profile, organizations, agreements, and folders available through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote software without clear user approval.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and check agent-skill synchronization settings before setup.

Risk: The connected account can make Concord information available through the skill's read actions.

Mitigation: Confirm that OOMOL may access the relevant Concord information before using the connected account.

## Reference(s):

- [Concord](https://www.concord.app/)
- [Concord API documentation](https://help.concord.app/hc/en-us/articles/360055115911-getting-started-with-the-concord-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON action results with text summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested Concord read action.]

## Skill Version(s):

1.0.4 (source: frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
