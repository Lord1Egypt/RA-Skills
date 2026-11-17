## Description:

Automates browser visits with Playwright to retrieve page titles and capture screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1393368499](https://clawhub.ai/user/1393368499)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate simple browser tasks, including visiting a URL, reading the page title, and saving a screenshot for downstream inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser egress can visit arbitrary URLs, including internal, localhost, metadata-service, authenticated, or sensitive pages.

Mitigation: Run only in an environment where broad browser egress is acceptable, and restrict provided URLs to non-sensitive external pages.

Risk: Screenshots may contain sensitive page content and are written to a predictable shared /tmp path without cleanup.

Mitigation: Treat screenshot outputs as sensitive, isolate the runtime, and delete or move /tmp/screenshot.png immediately after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1393368499/skills/my-browser-agent)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [JSON object containing status text, page titles, errors, and screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are written to /tmp/screenshot.png when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
