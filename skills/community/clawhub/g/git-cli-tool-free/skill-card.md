## Description:

Provides Git CLI quick references, repository status checks, staging and commit guidance, branch management, and remote sync guidance for developers working in command-line Git workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to get Git command guidance, inspect repository state, stage and commit changes, manage branches, and sync with remotes through an agent with shell command capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run repository-changing Git commands such as staging, committing, pushing, branch deletion, or force-with-lease pushes.

Mitigation: Require the agent to show status and diffs first, then confirm exact files, branch, remote, and commit message before any commit, push, or destructive branch operation.

Risk: Broad trigger language may cause the skill to be used during general coding or deployment requests where Git changes were not explicitly requested.

Mitigation: Use the skill only for explicit Git workflows and require confirmation before write, commit, push, or remote synchronization commands.

Risk: Credential helper guidance can store HTTPS credentials globally.

Mitigation: Avoid global credential storage unless the user understands how Git stores those credentials; prefer approved credential managers or SSH-based authentication.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository-changing Git command proposals or execution results; users should review status and diffs before changes are made.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
