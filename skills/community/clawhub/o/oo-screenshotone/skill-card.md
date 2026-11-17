## Description:

Operate ScreenshotOne through an OOMOL-connected account to check usage and devices and to capture screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check ScreenshotOne usage and available devices, and to submit still, animated, or bulk screenshot captures through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer and live connector behavior have not been verified, and installation may add other agent skills.

Mitigation: Review and approve the CLI installation, including any additional skills it installs, before use.

Risk: Some chargeable capture actions are treated as reads; animated and bulk captures can incur charges and send submitted content to OOMOL and ScreenshotOne.

Mitigation: Confirm the capture content, request count, and expected cost before animated or bulk submissions; avoid sending private content unless approved.

## Reference(s):

- [ScreenshotOne API documentation](https://screenshotone.com/docs/)
- [ScreenshotOne](https://screenshotone.com)
- [OOMOL oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Files, Guidance]

**Output Format:** [CLI commands with JSON payloads and connector response data; screenshot, GIF, or video capture files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Capture requests can include submitted page content and may use provider quota or incur costs.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
