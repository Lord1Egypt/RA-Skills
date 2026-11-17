## Description:

Generates structured GitHub repository digests with briefing summaries, categorized changes, community discussions, and clickable source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roggeohta](https://clawhub.ai/user/roggeohta)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to summarize recent activity in GitHub repositories, including releases, merged pull requests, open issues, breaking changes, and community discussion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private repository activity through the user's authenticated GitHub CLI session.

Mitigation: Use it only with repositories whose release, pull request, and issue activity is intended to be summarized.

Risk: Generated digests may include private or sensitive repository details.

Mitigation: Review the digest before sharing it outside the audience authorized to see the source repository activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roggeohta/skills/github-digest)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Analysis]

**Output Format:** [Markdown digest with clickable GitHub source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the authenticated GitHub CLI to read requested repository releases, pull requests, and issues.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
