## Description:

Manage Mac disk space by checking usage, cleaning junk, finding large files, and removing duplicates with explicit confirmation before deletions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukongsheld](https://clawhub.ai/user/wukongsheld)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use MacCleaner to check macOS disk usage, scan cleanup categories, identify large or duplicate files, and guide confirmed cleanup actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill auto-installs an unverified remote executable and persistently modifies Claude plugin configuration.

Mitigation: Review before installing; prefer a versioned, checksum-verified installer or manual plugin setup with clear uninstall instructions.

Risk: The skill can guide cleanup and file deletion workflows that may remove user data.

Mitigation: Keep the documented explicit user selection and confirmation steps before any cleanup or deletion action, and report results after the operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wukongsheld/skills/mac-cleanup-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, confirmation prompts, shell command blocks, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit confirmation before cleanup or deletion workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
