## Description:

Manage a single GitHub repository through chat by using a temporary GitHub token to check status, summarize recent activity, and create or follow up on issues and pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamkalio](https://clawhub.ai/user/iamkalio)

### License/Terms of Use:


## Use Case:

External users and non-technical requesters use this skill to get lightweight GitHub repository assistance in a chat workflow. It helps an agent gather repository context, summarize contributor activity, and draft or update issues and pull request follow-ups through the GitHub API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub tokens shared in chat may grant broad repository access if they are long-lived or over-scoped.

Mitigation: Use only fine-grained, repository-limited, short-lived tokens and avoid pasting tokens into normal chat where possible.

Risk: Repository data or secrets may be exposed if examples using /tmp caches or plaintext environment files are copied for private repositories.

Mitigation: Use a private per-session temporary directory, clean it up after use, and do not store long-lived tokens in plaintext env files.

Risk: Issue creation, issue updates, or comments can change a live repository workflow.

Mitigation: Require explicit user confirmation before creating or updating issues, changing issue state, assigning owners, or posting comments.

## Reference(s):

- [GitHub API Cheatsheet](references/github-api-cheatsheet.md)
- [GitHub REST API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub API request examples, repository summaries, issue drafts, status notes, and links returned by GitHub.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
