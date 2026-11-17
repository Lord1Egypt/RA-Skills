## Description:

Check for existing issues and PRs before creating new ones; the skill fires automatically when an agent intends to file an issue, open a PR, or comment on a thread, then searches the target repository for likely duplicates so the agent can decide whether to proceed or contribute to an existing thread instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[semmyt](https://clawhub.ai/user/semmyt)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill before filing GitHub issues, opening pull requests, or commenting on existing threads. It helps reduce duplicate reports by checking related issues and pull requests and presenting possible matches for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the existing GitHub CLI session, so repository visibility matches the authenticated user's current GitHub access.

Mitigation: Run it only with GitHub accounts and repository access appropriate for the work being performed.

Risk: Keyword searches can miss duplicate threads or return only loosely related issues and pull requests.

Mitigation: Review the returned titles, states, and comments before deciding whether to create a new thread, comment on an existing one, or reference a related item.

## Reference(s):

- [Overlap Check on ClawHub](https://clawhub.ai/semmyt/skills/overlap-check)
- [semmyt publisher profile](https://clawhub.ai/user/semmyt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline GitHub CLI commands and concise match summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GitHub CLI and uses the current GitHub session's repository visibility.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
