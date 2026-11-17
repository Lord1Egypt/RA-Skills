## Description:

Interact with Moodle LMS to browse courses, access learning materials, and answer questions about course content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4strium](https://clawhub.ai/user/4strium)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and agents use this skill to configure access to a Moodle LMS, list courses, inspect course content, search learning materials, download files, and answer questions using retrieved course materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external Moodle CLI binary while server-resolved provenance is unavailable.

Mitigation: Review the publisher and release provenance before installation, verify the published checksum, and only run the binary if the release is trusted.

Risk: Moodle passwords, tokens, or SSO token URLs could be exposed through shell commands or chat transcripts.

Mitigation: Prefer the interactive configuration flow, avoid entering secrets directly in commands or transcripts, and confirm where credentials are stored.

Risk: Whole-course syncs can bulk-download potentially sensitive course materials.

Mitigation: Choose the destination deliberately and avoid --no-confirm until the download scope has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4strium/skills/moodle-claw)
- [Project repository](https://github.com/4strium/moodle-claw)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; Moodle CLI commands can return JSON, human-readable text, extracted document text, or downloaded files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache Moodle course files locally after download.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
