## Description:

Safe-by-default music library organizer for scanning, planning, user-confirmed moves, soft deletion, verification, and cleanup of local music and lyric files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkcodee](https://clawhub.ai/user/thinkcodee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize local music libraries into an A-Z/artist/song structure, deduplicate by audio quality, match lyrics, and review dry-run plans before applying file moves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk file operations can move, rename, or misclassify files across a local music library.

Mitigation: Run dry-run mode first, review the generated plan, keep a backup, and execute only after explicit confirmation.

Risk: The release evidence flags unsafe deletion, permission, and install guidance, including rm -rf, chmod -R, and system Python package installation examples.

Mitigation: Avoid irreversible deletion and broad permission changes, use a virtual environment for dependencies, and run scripts as a low-privilege user scoped to the intended media directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thinkcodee/skills/music-library-organizer)
- [README](artifact/README.md)
- [Scripts README](artifact/scripts/README.md)
- [organize_music.py Usage Guide](artifact/scripts/organize_music.README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dry-run CSV reports and operation logs when the bundled scripts are executed]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
