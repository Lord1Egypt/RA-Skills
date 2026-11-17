## Description:

Configures JFTech device on-screen display settings, including channel titles, timestamp overlays, and privacy mask regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with JFTech OpenAPI credentials use this skill to query and update OSD settings on bound online devices, including channel titles, timestamp overlays, and privacy regions.

### Deployment Geography for Use:

China Mainland (CN), Asia (AS), Europe (EU), and North America (NA)

## Known Risks and Mitigations:

Risk: JF_ENDPOINT can redirect device tokens and signed API metadata to an untrusted host.

Mitigation: Set JF_ENDPOINT only to the documented JF regional API hosts and rotate the device token if it may have been used with an untrusted endpoint.

Risk: State-changing OSD actions can modify a live device's channel title or visibility overlays.

Mitigation: Confirm the target device, channel, action, title, and region values before running set operations; query current configuration first when practical.

Risk: The skill requires JF credentials and device tokens to execute API calls.

Mitigation: Use trusted credentials, keep secrets out of shared transcripts and logs, and scope execution to devices the operator is authorized to manage.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-device-osd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide state-changing OSD actions that use JF credentials, device tokens, device serial numbers, and regional API endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
