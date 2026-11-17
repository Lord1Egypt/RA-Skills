## Description:

Live markdown viewer for AI pair-editing. When you collaborate, the updates render instantly. Works with any AI agent and web browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:


## Use Case:

Developers and AI pair-editing users use this skill to install and run a local Markdown preview server so Markdown files render live in a browser while an agent edits them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable global npm command.

Mitigation: Prefer a pinned or locally reviewed package version before installing.

Risk: The local Markdown server can read broadly from the user's filesystem by default.

Mitigation: Run it only for trusted workspaces and start it with --root set to the directory intended for preview.

Risk: A background preview server may remain running after use.

Mitigation: Stop the background server when the preview session is finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/markdown-viewer)
- [wipcomputer/wip-markdown-viewer](https://github.com/wipcomputer/wip-markdown-viewer)
- [@wipcomputer/markdown-viewer npm package](https://www.npmjs.com/package/@wipcomputer/markdown-viewer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation and browser-launch guidance for a local Markdown preview workflow.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
