## Description:

Manage Overleaf LaTeX projects through git workflows, local LaTeX compilation, resume version branches, and optional native OpenClaw plugin tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to clone, branch, edit, compile, and push Overleaf-hosted LaTeX projects, especially tailored resume versions. Agents can use it to propose safe git and LaTeX workflows while checking credentials, connectivity, and local compilation before publishing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores Overleaf credentials in a local plaintext file.

Mitigation: Prefer a revocable Overleaf token instead of a password, restrict the credentials file to mode 600, and rotate the token if the workstation or file is exposed.

Risk: The setup recommends global git credential storage.

Mitigation: Use a scoped credential helper or OS keychain instead of enabling plaintext global credential storage.

Risk: The suggested OpenClaw plugin install is unpinned third-party executable code.

Mitigation: Review and pin the plugin separately before installation, and treat it as a separate trust decision from this skill.

Risk: The workflow can push local changes to Overleaf projects.

Mitigation: Compile locally, review git diffs, pull remote web edits first, and avoid force-pushing to protected base branches.

## Reference(s):

- [LaTeX Resume Patterns](references/latex-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, git, and LaTeX examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow guidance for Overleaf git access, local compilation, branch management, and a local health-check script.]

## Skill Version(s):

1.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
