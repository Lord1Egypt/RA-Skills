## Description:

Download encrypted m3u8/HLS videos using parallel downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and media operators use this skill to extract HLS playlist information, download video segments in parallel, and assemble m3u8 streams into MP4 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe output names can cause deletion or overwriting outside the intended download area.

Mitigation: Review before installing, pass only a simple filename-only output name, and avoid running the script in sensitive directories or environments.

Risk: Untrusted playlist URLs can trigger downloads from unexpected locations.

Mitigation: Use only trusted m3u8 URLs and restrict URL schemes and redirects before deployment.

Risk: Cleanup may remove the wrong path if the working directory is not safely constructed.

Mitigation: Use a temporary directory created with mktemp and clean up only a verified directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/easonc13/skills/m3u8-downloader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and commands for downloading HLS segments and saving a final MP4 file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
