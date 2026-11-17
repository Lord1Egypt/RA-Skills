## Description:

Guides agents through Git commits, pull requests, and releases using conventional commits, semantic versioning, optional GitHub CLI workflows, and commit-message validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create focused commits, draft pull requests, and prepare releases with consistent messages, changelog updates, tags, and GitHub release commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to push commits to a remote repository automatically after committing.

Mitigation: Install it only where immediate publication is intended; otherwise require explicit approval before git push, creating upstream branches, pushing tags, creating pull requests, or publishing releases.

## Reference(s):

- [Git Workflow ClawHub page](https://clawhub.ai/niracler/skills/nini-git-workflow)
- [Examples and Templates](references/examples-and-templates.md)
- [Git documentation](https://git-scm.com/)
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Release v0.3.0](https://github.com/niracler/skill/releases/tag/v0.3.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run git commands that change repository state and publish commits, tags, pull requests, or releases.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
