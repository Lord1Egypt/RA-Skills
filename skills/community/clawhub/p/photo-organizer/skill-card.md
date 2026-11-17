## Description:

A photo organization skill that helps users batch-sort images by capture date or available location metadata, preview planned changes, and undo completed organization runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to organize large photo folders into date- or location-based directory structures, with preview and undo workflows for safer file handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The undo workflow can copy and delete files based on a backup manifest.

Mitigation: Use the script only on directories you control and do not run undo when .photo-organizer-backup.json could have been modified by someone else.

Risk: One documented install path uses an unverified package source.

Mitigation: Prefer the ClawHub release or verify package ownership and version before using the pip install path.

Risk: The tool changes local photo organization and may affect large batches of files.

Mitigation: Run preview first and keep a separate backup of original photos before executing organization commands.

## Reference(s):

- [Photo Organizer README](artifact/README.md)
- [Photo Organizer Skill Page](https://clawhub.ai/utopiabenben/skills/photo-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe preview, organization, and undo workflows for local photo files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
