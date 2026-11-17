## Description:

Analyze, triage, and select the best issues to work on from GitHub repositories. Scores issues by reproducibility, scope, complexity, and community signal. Produces a structured analysis document with root cause hypotheses and fix approaches. Use when deciding which issues to tackle in open-source projects, prioritizing a backlog, or analyzing bug reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliverp](https://clawhub.ai/user/sliverp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and engineering teams use this skill to triage GitHub issue backlogs, score candidate issues, and produce a structured analysis document with root cause hypotheses and fix approaches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub tokens or repository access details may be exposed if users paste credentials into chats, project files, logs, or shared output.

Mitigation: Use the GitHub CLI secure login flow when possible. If a token is needed, use a fine-grained read-only token for the repositories being analyzed, keep it out of chats and files, and redact it from logs and shared output.

Risk: The generated issue analysis may prioritize work from incomplete issue context or miss an existing maintainer decision or pull request.

Mitigation: Review the full issue thread, related pull requests, maintainer comments, and repository context before acting on selected candidates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sliverp/skills/issue-hunter)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Shell commands, Guidance]

**Output Format:** [Markdown document with tables, issue scores, root cause hypotheses, and fix approaches]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces issue-analysis.md in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
