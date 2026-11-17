## Description:

Access Jamie meeting data through a connected account, including meeting search, details, tasks, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Jamie for recorded meetings can search meetings and retrieve details, summaries, transcripts, action items, and tags through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an unverified remote installer payload.

Mitigation: Review the dependency installation and use a fixed, verified oo CLI release before enabling the skill.

Risk: Startup skill synchronization may install or change skills in other agents.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 unless cross-agent skill synchronization is intended.

Risk: The connected service can access private meeting content in the Jamie account.

Mitigation: Connect only the Jamie account intended for these queries and consider OOMOL's access to its private meeting content.

## Reference(s):

- [Jamie homepage](https://www.meetjamie.ai)
- [Jamie API documentation](https://docs.meetjamie.ai/developers/api/getting-started)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [Structured Jamie meeting and task data in JSON, with text summaries where provided]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data depends on the selected action and the connected Jamie account.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
