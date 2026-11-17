## Description:

Interface with Google's Jules Tools CLI to manage AI coding sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexdavidswift](https://clawhub.ai/user/alexdavidswift)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to guide an agent through installing and authenticating the Jules CLI, then listing, starting, and pulling remote Jules coding sessions from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends an unpinned global npm install with an optional sudo fallback.

Mitigation: Prefer a pinned or user-scoped Jules CLI installation and avoid sudo unless the package and system-level impact have been independently reviewed.

Risk: Pulling remote session results can introduce code changes into the workspace.

Mitigation: Run pull commands in a clean branch or disposable workspace and inspect the resulting diff before executing or merging the code.

## Reference(s):

- [Google Jules CLI reference](https://jules.google/docs/cli/reference/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces terminal-oriented instructions for installing, authenticating, listing sessions, creating sessions, and pulling Jules session results.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
