## Description:

Download PhotoPlus live albums from a URL or activity ID, inspect metadata, filter date tabs, save JSON, and write caption or GPS metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloene](https://clawhub.ai/user/helloene)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download or inspect public PhotoPlus album contents when they have permission to store the photos. It helps agents prepare the wrapper command, choose metadata options, and report the output folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run mutable third-party downloader code and install unpinned Python packages.

Mitigation: Review before installing, use a disposable or constrained environment, avoid --install-deps in shared Python environments, and prefer a vetted local checkout pinned to the documented commit or another trusted commit.

Risk: The skill downloads album contents that may belong to another party.

Mitigation: Confirm the user has permission to download and store the album contents before running the downloader.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloene/skills/photoplus-album-downloader)
- [Upstream project homepage](https://github.com/helloene/live-album-downloader)
- [Upstream project notes](artifact/references/upstream-project.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated local photo folders, JSON metadata sidecars, and EXIF/IPTC metadata options.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
