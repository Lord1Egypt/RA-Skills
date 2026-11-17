## Description:

Upload image files to PixelVault and get a public CDN URL back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[facundofarias](https://clawhub.ai/user/facundofarias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload screenshots, diagrams, charts, and other image artifacts to PixelVault so they can share permanent CDN URLs in pull requests, issues, comments, and related collaboration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images become permanent public CDN URLs and may expose screenshots, diagrams, or build artifacts that contain secrets or private data.

Mitigation: Confirm each upload with the user and inspect files for sensitive content before sending them to PixelVault.

Risk: The skill uses local shell commands and file paths, including glob patterns, to invoke the PixelVault CLI.

Mitigation: Avoid blindly passing user-provided paths through a shell; prefer explicit paths and review the resolved file list before upload.

Risk: The artifact recommends installing a global CLI before upload.

Mitigation: Prefer a pinned, locally scoped CLI installation where possible and verify PixelVault authentication before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/facundofarias/skills/pixelvault-upload)
- [Publisher profile](https://clawhub.ai/user/facundofarias)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and returned CDN URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one permanent CDN URL per uploaded file; JSON metadata can be requested from the CLI when needed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
