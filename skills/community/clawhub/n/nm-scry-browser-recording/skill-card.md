## Description:

Records browser sessions with Playwright and guides conversion to GIFs for web UI demos and tutorials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and tutorial creators use this skill to run Playwright specs that capture web UI workflows as videos, then prepare recordings for GIF conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings may capture credentials or personal information shown in browser pages.

Mitigation: Use sanitized pages and accounts, and review recordings before sharing.

Risk: The package-version concern was flagged but disputed, and the scanner review was partial because some referenced paths were absent from the bundle.

Mitigation: Review dependency versions and the complete installed skill bundle before running recordings.

## Reference(s):

- [Spec execution guide](modules/spec-execution.md)
- [Video capture guide](modules/video-capture.md)
- [Homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/scry)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-scry-browser-recording)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, Video recordings]

**Output Format:** [Markdown guidance with shell commands and TypeScript configuration examples; Playwright WebM recordings, with GIF conversion handled by the companion skill.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video resolution, viewport, recording duration, and GIF conversion settings can be adjusted.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
