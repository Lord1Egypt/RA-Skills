## Description:

Route OraHub image edit requests to the right Ora workflow for color matching, passersby removal, background cutout, and background replacement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orahub-ora](https://clawhub.ai/user/orahub-ora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route practical photo-editing requests into the correct OraHub workflow, including reference-based color matching, background people removal, transparent PNG cutouts, and background replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running an unpinned global OraHub CLI.

Mitigation: Approve the CLI install only when the package and publisher are trusted, and prefer a pinned or audited version when available.

Risk: Workflow commands use user-provided paths, URLs, and output locations.

Mitigation: Treat image paths and URLs as data, reject suspicious shell metacharacters and non-public URLs, and run with the least filesystem access needed.

Risk: The security verdict recommends review before installation.

Mitigation: Review the skill and its OraHub CLI dependency before deployment, then follow the package guidance for authentication and execution approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orahub-ora/skills/orahub-skills)
- [Platform compatibility reference](references/platform-compatibility.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown or text replies with OraHub CLI commands, JSON command output, and local image file or MEDIA path delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the orahub CLI and authentication; image workflows may produce PNG or source-extension image files depending on the selected leaf skill.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
