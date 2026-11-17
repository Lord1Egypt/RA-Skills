## Description:

Cut, trim, concatenate, and split video files - basic video editing operations

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and technical operators use this skill to get FFmpeg command guidance for cutting, trimming, concatenating, splitting, and extracting video segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FFmpeg commands may overwrite or create files in the workspace or chosen output path.

Mitigation: Review output paths before running commands and use explicit filenames or a scratch directory for edited media.

Risk: Concatenation examples rely on media files and list files supplied by the user.

Mitigation: Use only trusted media and list files, and inspect concat lists before passing them to FFmpeg.

Risk: Fast copy-based cuts and concatenation can be less precise or require matching codecs and formats.

Mitigation: Use the re-encoding examples when precision or codec compatibility matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local FFmpeg command examples that should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
