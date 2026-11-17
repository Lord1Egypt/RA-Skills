## Description:

Java Code Review helps developers review GitLab branch or commit changes before merge, assess Security, Performance, Correctness, Maintainability, and Testing concerns, generate a CR report, track fixes, and execute a merge only after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyuzhy](https://clawhub.ai/user/zhouyuzhy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Java changes in GitLab before merging branches or inspecting individual commits. It produces a structured CR report with severity-ranked findings, author attribution, pass items, and merge guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitLab credentials may grant repository access beyond the review task.

Mitigation: Use a least-privilege token, keep credentials out of reviewed source and generated reports, and confirm the token source before API use.

Risk: The workflow includes repository-changing merge actions after review.

Mitigation: Verify the project, source branch, and target branch, prefer merge requests over direct commits, and require explicit user confirmation before any merge.

Risk: Automated review findings can be incomplete or overly broad.

Mitigation: Have a qualified reviewer validate CR findings and require Critical or High issues to be resolved before merging.

## Reference(s):

- [Code Review Checklist](references/checklist.md)
- [GitLab API Reference](references/gitlab-api.md)

## Skill Output:

**Output Type(s):** [markdown, guidance, API calls, shell commands]

**Output Format:** [Markdown CR report with GitLab API request examples and merge guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include severity-ranked findings, affected file and line references, commit author attribution, pass items, and a merge recommendation.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
