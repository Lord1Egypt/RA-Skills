## Description:

Use when managing Halo posts or single pages from the terminal, including list, get, create, update, delete, open, export-json, import-json, categories, tags, and content files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruibaby](https://clawhub.ai/user/ruibaby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to have an agent manage Halo posts, post categories, post tags, and single pages through the Halo CLI. It supports listing, inspecting, creating, updating, deleting, opening, and importing or exporting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run destructive Halo content actions such as deletes or forced imports.

Mitigation: Review delete and force-import commands before execution, read current state when the target is uncertain, and use `--json` outputs for automation checks.

Risk: A misconfigured Halo profile can apply content changes to the wrong site.

Mitigation: Check the active authentication context and pass the intended `--profile` when more than one Halo profile is configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruibaby/skills/halo-cli-content)
- [halo-cli-shared](../halo-cli-shared)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Halo CLI commands and content-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON and Markdown content files used by Halo import and export workflows.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
