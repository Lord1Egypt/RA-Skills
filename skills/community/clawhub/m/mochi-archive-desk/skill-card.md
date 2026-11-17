## Description:

Inspect ZIP/TAR contents, extract into new folders, create ZIPs from selected files and report per-file integrity hashes. Use for Archive and Integrity Toolbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and other agent users use this skill to inspect ZIP/TAR archives, extract contents into new folders, create ZIPs from explicit file lists, and verify files with SHA-256 hashes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted archive contents may be unsafe to open.

Mitigation: Extract into a new folder, then review the manifest and contents before opening files.

Risk: Installing the latest release may introduce unreviewed changes.

Mitigation: Use a reviewed installer version instead of @latest.

Risk: Local .mochilab state persists after use.

Mitigation: Avoid including this private state folder in shared Skill packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-archive-desk)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [ZIP archives or extracted files, with JSON operation receipts and SHA-256 manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archive input and expanded data are limited to 100 MiB and 5,000 entries.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
