## Description:

Implements GitHub or GitLab issues via parallel subagents with review gates between task batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve GitHub, GitLab, or Bitbucket issues, plan and implement changes with review gates, and consolidate the work into one pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may publish tooling feedback containing details derived from a work session to an unrelated external repository.

Mitigation: Review the external feedback step before execution; skip it or redact details if sharing is not acceptable for the session.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-do-issue)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Markdown, Guidance]

**Output Format:** [Repository changes, forge CLI commands, and Markdown progress and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May comment on or close issues and open one consolidated pull request; requires the configured git-platform detector and supporting planning, testing, review, and branch-finishing skills.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
