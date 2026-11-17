## Description:

Publishes the current project to a GitHub remote by resolving the repository URL, initializing Git when needed, committing local changes, and pushing the current branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish a local project to a GitHub repository through an agent-assisted Git workflow. It is intended for repository initialization, remote setup, committing local changes, branch detection, pushing, and remembering project-to-repository mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stage, commit, and push broad local changes, which may publish secrets, private data, or unfinished work.

Mitigation: Inspect git status and diffs before execution, maintain a strict .gitignore, and avoid running it in repositories containing secrets, customer data, or sensitive work-in-progress.

Risk: The skill can set or change the origin remote and may offer force push after push failures, which can publish to the wrong repository or overwrite remote history.

Mitigation: Confirm the resolved remote URL, current branch, and push mode before allowing the agent to push or force push.

Risk: The skill persists local project-to-repository mappings and includes self-evolution behavior that may write follow-up notes or propose changes beyond the publish task.

Mitigation: Review or remove repo-map persistence and self-evolution behavior before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orbisz/skills/git-publish-skill)
- [repo-map.json](references/repo-map.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Git commits, configure or change the origin remote, push branches, and update the repository mapping file when executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
