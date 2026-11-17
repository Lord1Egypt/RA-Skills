## Description:

Manage notes, bookmarks, and notebooks using the nb CLI. Create, list, search, and organize notes across multiple notebooks with Git-backed versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjesuiter](https://clawhub.ai/user/bjesuiter)

### License/Terms of Use:


## Use Case:

Developers and command-line users use this skill to manage nb notes, bookmarks, todos, notebooks, and Git-backed synchronization through nb CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct writes into ~/.nb notebooks could bypass nb indexing and commit unintended files.

Mitigation: Prefer nb CLI commands for add, edit, delete, checkpoint, and sync operations; avoid manual writes into ~/.nb unless explicitly reviewed.

Risk: Notebook Git commits or sync operations may expose sensitive notebook contents or unexpected remote changes.

Mitigation: Review configured remotes, avoid storing secrets in notebooks, and inspect staged changes before any manual Git commit or sync.

## Reference(s):

- [nb GitHub repository](https://github.com/xwmx/nb)
- [ClawHub skill page](https://clawhub.ai/bjesuiter/skills/nb)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes the nb CLI is installed on macOS or Linux.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
