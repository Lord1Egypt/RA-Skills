## Description:

Converts MP4 video files to GIF format with ffmpeg using a two-pass palette method and quality/size controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzlupus](https://clawhub.ai/user/zzlupus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation authors, and content creators use this skill to convert local MP4 or other video clips into GIFs. It helps tune frame rate and width to balance image quality, motion smoothness, and output file size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted local video inputs can exercise ffmpeg parsing paths during conversion.

Mitigation: Use the skill with trusted local video files and keep ffmpeg current.

Risk: Unvalidated width or FPS values can produce failed conversions or unexpectedly large GIF files.

Mitigation: Use normal numeric width and FPS values, and prefer adding explicit numeric validation before broad deployment.

Risk: Temporary palette files are created during conversion, which may be less appropriate in shared hostile temporary-directory environments.

Mitigation: Avoid shared hostile temp directories and prefer private temporary directories for hardened deployments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline Bash, PowerShell, and ffmpeg command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg installed on the local system; bundled Bash and PowerShell scripts accept input file, output file, width, and FPS parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
