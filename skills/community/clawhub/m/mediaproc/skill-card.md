## Description:

Processes video, audio, and images through a configured SSH media-processing container using ffmpeg, sox, and ImageMagick.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media creators use this skill to transfer files to a trusted media-processing instance, transcode and inspect video or audio, manipulate images, and retrieve results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured host can see transferred media and commands.

Mitigation: Use only an instance you control or trust, and prevent untrusted changes to MEDIAPROC_HOST and MEDIAPROC_PORT.

Risk: Remote file and directory deletion is permanent.

Mitigation: Require explicit confirmation of the exact path before remove-file, remove-dir, or remove-dir-recursive.

Risk: The optional server installer runs with elevated privileges.

Mitigation: Pin the installer to a release and review it before running it with sudo.

## Reference(s):

- [mediaproc on ClawHub](https://clawhub.ai/psyb0t/skills/mediaproc)
- [mediaproc project homepage](https://github.com/psyb0t/docker-mediaproc)
- [mediaproc setup](references/setup.md)
- [lockbox container](https://github.com/psyb0t/docker-lockbox)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, Text]

**Output Format:** [Markdown guidance and shell commands; processed media files or text and JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SSH access to a trusted instance configured with MEDIAPROC_HOST and MEDIAPROC_PORT.]

## Skill Version(s):

2.0.13 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
