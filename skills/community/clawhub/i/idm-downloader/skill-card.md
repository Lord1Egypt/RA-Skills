## Description:

Download large files using IDM (Internet Download Manager) on Windows when a user provides a URL and wants IDM-based downloading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxcatt](https://clawhub.ai/user/foxcatt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users on Windows use this skill to start IDM downloads from URLs, optionally choosing an output directory and filename. It is suited to large files where IDM download acceleration and resumption are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start downloads from user-provided URLs and write to a user-selected output path.

Mitigation: Review the target URL and output path before running the downloader.

Risk: The optional pywin32 dependency enables Windows COM automation for IDM.

Mitigation: Install pywin32 only from a trusted, pinned source, preferably in a virtual environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/foxcatt/skills/idm-downloader)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and guidance for launching IDM downloads; actual file transfer is performed by the local IDM installation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
