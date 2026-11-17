## Description:

Extracts Simplified Chinese and English text subtitle tracks from MKV files, merges them into bilingual subtitles with English above Chinese, and embeds the merged track back into MKV output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media automation users use this skill to process MKV files that contain separate Chinese and English text subtitle tracks, producing a bilingual subtitle track and embedding it into a new or updated MKV file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can replace source MKV files in place when no output path is provided.

Mitigation: Run with --dry-run first, provide --output for side-by-side files, and keep backups before processing valuable media.

Risk: Batch and recursive processing can apply in-place changes to many files.

Mitigation: Confirm the exact file list before batch execution and avoid recursive runs unless the target tree has been reviewed.

Risk: The tool depends on local MKVToolNix commands and text subtitle tracks.

Mitigation: Install and verify mkvmerge and mkvextract, and use it only with supported SRT, ASS, or SSA subtitle tracks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlalamoon/skills/mkv-bilingual-subtitle)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated MKV subtitle output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MKVToolNix command-line tools and supports SRT, ASS, and SSA text subtitles.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
