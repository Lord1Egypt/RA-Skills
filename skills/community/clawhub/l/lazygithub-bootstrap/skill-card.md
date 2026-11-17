## Description:

Publish, bootstrap, or tidy a GitHub repository so the README and full GitHub About metadata stay in sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjo92](https://clawhub.ai/user/hanjo92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, publish, or tidy GitHub repositories with a README, description, homepage when available, and useful repository topics. It is intended for repository setup and metadata synchronization tasks driven through GitHub CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or modify GitHub repositories, including public remote changes, without strong confirmation or path-safety controls in the wrapper script.

Mitigation: Confirm the owner, repository name, visibility, source directory, files to be pushed, and absence of secrets before any GitHub CLI command runs.

Risk: The wrapper script defaults to public visibility and can scaffold, initialize, commit, create, and push a repository.

Mitigation: Avoid the wrapper script unless it is updated to reject unsafe paths and require an explicit public or private visibility choice.

## Reference(s):

- [Prompt Templates](references/prompt-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/hanjo92/skills/lazygithub-bootstrap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and repository metadata summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run GitHub CLI commands that create repositories, push local content, and edit public repository metadata.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
