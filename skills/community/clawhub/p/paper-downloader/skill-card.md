## Description:

Downloads a user-supplied file URL and returns a local path for later processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anonymous9n23](https://clawhub.ai/user/anonymous9n23)

### License/Terms of Use:

MIT-0

## Use Case:

People collecting research papers or other files use this skill to download a URL and pass the saved path to another skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded content can be saved to the filesystem root and overwrite an existing file.

Mitigation: Restrict saves to /tmp/skill-downloads, prevent overwrites, and use minimal filesystem privileges.

Risk: Unsafe URLs or redirects can access unintended destinations, and downloads lack an enforced size limit.

Mitigation: Reject unsafe URLs and redirects, enforce the 64 MiB limit while streaming, and use minimal network privileges.

## Reference(s):

- [Paper Downloader on ClawHub](https://clawhub.ai/anonymous9n23/skills/paper-downloader)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain-text local file path and downloaded file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The current script saves under the filesystem root, not the stated download directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
