## Description: <br>
Process media files (video, audio, images) via a locked-down SSH container with ffmpeg, sox, and imagemagick. Use when the user wants to transcode video, process audio, manipulate images, or work with media files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to process video, audio, and image files through a configured mediaproc SSH container, including transcoding, inspection, thumbnail creation, normalization, and file management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions include running an unpinned remote installer as root. <br>
Mitigation: Download and inspect the installer first, prefer a pinned release or commit, and verify integrity before running it with elevated privileges. <br>
Risk: The skill sends media files and commands to a configured SSH host. <br>
Mitigation: Install only when the docker-mediaproc project and configured host are trusted, use a dedicated SSH key, and avoid exposing the mediaproc port broadly. <br>
Risk: Management commands can remove files or uninstall the mediaproc environment. <br>
Mitigation: Back up important work before destructive file operations, recursive directory removal, or uninstall. <br>


## Reference(s): <br>
- [mediaproc setup](references/setup.md) <br>
- [docker-mediaproc](https://github.com/psyb0t/docker-mediaproc) <br>
- [docker-lockbox](https://github.com/psyb0t/docker-lockbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended to run through scripts/mediaproc.sh against a configured mediaproc SSH host.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
