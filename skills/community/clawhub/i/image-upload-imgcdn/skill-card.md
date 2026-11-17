## Description:

Upload a local image to img.scdn.io and return a public permanent link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nujgnoix](https://clawhub.ai/user/nujgnoix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload a local image file and receive a public URL for sharing in posts or other public workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The uploaded image becomes public and permanent.

Mitigation: Use only for images intended for public sharing and avoid uploading private, sensitive, or regulated content.

Risk: The response parsing behavior has a remote-code-execution risk if the upload service returns malicious content.

Mitigation: Review before installation, trust the upload service before use, and fix response parsing to read JSON from stdin or a file without interpolating server responses into executable code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nujgnoix/skills/image-upload-imgcdn)
- [img.scdn.io upload endpoint](https://img.scdn.io/api/v1.php)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text public URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a permanent public URL when the upload succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
