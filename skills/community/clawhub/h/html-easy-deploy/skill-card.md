## Description:

Instantly deploy a single self-contained HTML page to htmlcode.fun for quick live URLs. Alias of html-deploy, with versioned updates, description-required deploys, and liked-version protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520xiaomumu](https://clawhub.ai/user/520xiaomumu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish, update, inspect, fetch, and manage single-file HTML pages on htmlcode.fun when fast sharing is more important than full project hosting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or version-management commands can change public htmlcode.fun content.

Mitigation: Review commands before deploy, overwrite, unpublish, delete, switch-current, or append operations, and confirm destructive or public-content changes with the user.

Risk: Fetching deployed content with --output can overwrite a local file path supplied to the script.

Mitigation: Check the output path before running get --output, especially when reusing filenames in the workspace.

Risk: Overwriting, unpublishing, or deleting an existing version can affect preserved work if the wrong version is targeted.

Mitigation: Inspect version history first and rely on the likeCount preflight; append a new version when the target version is liked or should be preserved.

## Reference(s):

- [htmlcode.fun live guide](https://www.htmlcode.fun/s/htmlcode-fun-guide)
- [htmlcode.fun service](https://www.htmlcode.fun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results from the bundled deployment script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write fetched HTML content to a user-specified local output path when using the get command.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
