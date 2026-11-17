## Description:

Autonomous GitHub Issue Resolver Agent with guardrails for discovering, analyzing, and fixing open GitHub issues from issue selection through draft pull request preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashwinhegde19](https://clawhub.ai/user/ashwinhegde19)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to discover open GitHub issues, analyze issue context, plan fixes, make scoped code changes, run tests, and prepare draft pull requests for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to fix GitHub issues, but the server security summary says its safety wrappers are under-enforced.

Mitigation: Use only after repo, branch, path, command, and approval checks are enforced at execution time.

Risk: The server security guidance warns that some scripts can run unsafe shell commands while using GitHub credentials.

Mitigation: Run it only in a disposable checkout with a tightly scoped GitHub account or token, and do not grant private repository or broad local file access.

Risk: PR creation and repository mutation can affect upstream projects if approvals are bypassed.

Mitigation: Require verified user approval before code changes, commits, pushes, or draft PR creation.

## Reference(s):

- [Guardrails Guide](references/guardrails-guide.md)
- [GitHub Issue Resolver Quick Reference](references/quick-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/ashwinhegde19/skills/github-issue-resolver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status updates with inline shell commands, JSON issue analysis, code changes, test results, and draft PR content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audit records and pull request metadata when the user approves those actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and guardrails.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
