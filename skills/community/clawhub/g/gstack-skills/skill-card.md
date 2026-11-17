## Description:

Complete development workflow suite that routes /gstack and related commands to specialized workflows for product ideation, code review, testing, QA, debugging, documentation, release preparation, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsg12te-del](https://clawhub.ai/user/dsg12te-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and run gstack-style workflows across product validation, planning, implementation review, QA, release, documentation, retrospective, and safety-check tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the local state manager can read, modify, or delete JSON files outside its intended folder through unvalidated workflow IDs.

Mitigation: Use the state manager only in trusted, single-user workspaces until workflow IDs are validated and state files are permission-restricted.

Risk: The workflow can inspect repositories, suggest or apply code fixes, and guide release workflows.

Mitigation: Require explicit confirmation before fixes, merges, PR creation, deployment, or state deletion, and review diffs before accepting changes.

Risk: Workflow state may expose sensitive project context if secrets are stored in local state files.

Mitigation: Do not store secrets in workflow state and clear state files when they are no longer needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dsg12te-del/skills/gstack-skills)
- [Original gstack project](https://github.com/garrytan/gstack)
- [Y Combinator](https://www.ycombinator.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and guidance with inline code or shell command blocks where workflows require them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route to specialized skills and may maintain local JSON workflow state when helper scripts are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter mentions 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
