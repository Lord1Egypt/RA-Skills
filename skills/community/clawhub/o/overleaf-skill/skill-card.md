## Description:

Sync and manage Overleaf LaTeX projects from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aloth](https://clawhub.ai/user/aloth)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and academic authors use this skill to guide command-line workflows for pulling, syncing, compiling, and packaging Overleaf LaTeX projects, including arXiv submission outputs such as .bbl files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires handling an Overleaf session cookie that can provide access to user projects.

Mitigation: Treat `overleaf_session2` like a password, avoid putting it in shell history, do not commit `.olauth`, and prefer a restricted environment variable or safer credential store when available.

Risk: The installation path uses mutable third-party CLI packages distributed through Homebrew or npm.

Mitigation: Install only if the publisher is trusted, and pin or independently audit the `olcli` package before using it with sensitive projects.

Risk: Sync and push commands can change files in an Overleaf project.

Mitigation: Review local changes before syncing, use dry-run behavior where available, and keep recoverable copies of important project files.

## Reference(s):

- [Overleaf API Reference](references/API.md)
- [Overleaf](https://www.overleaf.com)
- [olcli on npm](https://www.npmjs.com/package/@aloth/olcli)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for using olcli; it does not itself execute Overleaf operations.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
