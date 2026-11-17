## Description:

Sync and manage Overleaf LaTeX projects from the command line, including pull, push, PDF compilation, and compile-output downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aloth](https://clawhub.ai/user/aloth)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and academic authors use this skill to operate the olcli command-line tool for synchronizing Overleaf projects, compiling PDFs, and retrieving build artifacts such as .bbl files for arXiv submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle a live Overleaf session cookie, which can grant access to Overleaf projects if exposed.

Mitigation: Treat the overleaf_session2 cookie like a password: avoid shell history, shared terminals, logs, screenshots, project directories, and source control; revoke the browser session if it may have leaked.

Risk: The install workflow depends on the upstream olcli package and grants that tool access to Overleaf projects.

Mitigation: Install only if the upstream olcli package is trusted and review commands before executing them.

## Reference(s):

- [Overleaf API Reference](references/API.md)
- [olcli GitHub Repository](https://github.com/aloth/olcli)
- [@aloth/olcli npm Package](https://www.npmjs.com/package/@aloth/olcli)
- [Overleaf](https://www.overleaf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that authenticate with Overleaf, install olcli, sync project files, compile PDFs, and download compile outputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
