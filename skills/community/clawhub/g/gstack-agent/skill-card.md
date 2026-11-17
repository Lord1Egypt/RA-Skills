## Description:

GStack Agent coordinates product planning, engineering review, design review, QA, release, monitoring, documentation, and retrospective workflows through role-specific slash-command guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocbond](https://clawhub.ai/user/rocbond)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software teams use this skill to guide an agent through product discovery, architecture review, design critique, code review, QA, release, monitoring, benchmarking, documentation, and retrospectives for software-delivery work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make code changes or update project files during review, QA, documentation, and release workflows.

Mitigation: Use read-only workflows such as /qa-only when inspection is sufficient, review proposed edits before applying them, and keep normal version-control review in place.

Risk: The skill includes release and deployment workflows that can push branches, merge pull requests, deploy production, or revert changes.

Mitigation: Require explicit manual confirmation before git push, PR merge, deployment, revert, or updates to agent instruction files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rocbond/skills/gstack-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, commands, reports, and file-oriented deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform code edits, tests, release actions, deployment checks, and documentation updates depending on the invoked workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
