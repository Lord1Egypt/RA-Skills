## Description:

Batch removes promotional and descriptive ID3 metadata from MP3 files while aiming to preserve the audio stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangzhang888](https://clawhub.ai/user/haiyangzhang888)

### License/Terms of Use:

MIT-0

## Use Case:

People managing MP3 libraries use this skill to clean selected folders of MP3 files by preparing a file list, running a Windows tag-cleaning utility, and checking the resulting files. It is intended for removing ID3v1 and ID3v2 fields such as title, album, artist, comments, embedded art, and other text tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MP3 files may be overwritten or corrupted during metadata removal.

Mitigation: Run the skill only on backed-up copies or a disposable test folder, and verify sample output before processing a larger library.

Risk: An incorrect file list could modify unintended files.

Mitigation: Review the generated MP3 path list before execution and scope it to the intended folder.

Risk: Fixed temporary paths and a missing compiled executable can make runtime behavior unclear.

Mitigation: Confirm the executable or compile step, file-list path, and temporary working directory before running the tool.

## Reference(s):

- [MP3 Tag Cleaner ClawHub listing](https://clawhub.ai/haiyangzhang888/skills/mp3-tag-cleaner)
- [Publisher profile](https://clawhub.ai/user/haiyangzhang888)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with file paths and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets user-selected MP3 files and may invoke a Windows executable or C# compilation step.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
