## Description:

Analyze media files with MediaInfo CLI and compare behavior with ffprobe. Use when inspecting container/codec metadata, extracting width/height/duration/bitrate, troubleshooting files that ffprobe cannot parse, or classifying media by orientation (landscape/portrait).

This skill is ready for commercial/non-commercial use.

## Publisher:

[karlzhu-zxc](https://clawhub.ai/user/karlzhu-zxc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and run MediaInfo locally, inspect media container and codec metadata, compare results with ffprobe, and classify media orientation from width, height, and rotation fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs third-party build code without integrity verification.

Mitigation: Run installation only in a contained environment, pin and verify the source archive with checksum or signature validation, and avoid exposing credentials or sensitive files.

Risk: MEDIAINFO_URL can override the download source.

Mitigation: Use MEDIAINFO_URL only with a trusted archive source and validate the archive before running the build.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karlzhu-zxc/skills/media-info)
- [MediaInfo CLI source archive](https://mediaarea.net/download/binary/mediainfo/0.7.94/MediaInfo_CLI_0.7.94_GNU_FromSource.tar.bz2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and MediaInfo plain-text or JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local vendor and temporary test files when the bundled install or smoke-test scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
