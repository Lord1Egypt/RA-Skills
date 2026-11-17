## Description:

GitHub Knowledge Base helps agents maintain a local GitHub repository catalog and use the GitHub CLI to search repositories, issues, and pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameschan21](https://clawhub.ai/user/jameschan21)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to search GitHub with gh CLI, clone repositories into a local knowledge base, and maintain a GITHUB_KB.md project catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GitHub token may grant broader repository access than the workflow needs.

Mitigation: Use the least-privileged GitHub token needed and provide it through GITHUB_TOKEN or a secret manager rather than hardcoding it.

Risk: The local knowledge base may accumulate private or untrusted cloned repositories.

Mitigation: Set GITHUB_KB_PATH to an expected directory and review private or untrusted repositories before allowing them to persist in the KB.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jameschan21/skills/github-kb)
- [GitHub CLI Linux Installation Guide](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update a local GITHUB_KB.md catalog and propose gh CLI commands for GitHub search and cloning workflows.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
