## Description:

Imou/Lechange device video skill for live HLS, local and cloud record clips, and playback HLS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imou-openplatform](https://clawhub.ai/user/imou-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to obtain live HLS streams, query local or cloud recording clips, and create playback HLS URLs for Imou or Lechange device channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Imou app credentials, access tokens, device identifiers, and HLS URLs may expose camera access if mishandled.

Mitigation: Treat credentials and returned URLs as secrets; avoid logging, sharing, or storing them outside approved secret and incident-review workflows.

Risk: A user-controlled IMOU_BASE_URL can direct sensitive request data to an untrusted API endpoint.

Mitigation: Set IMOU_BASE_URL only to the official HTTPS Imou or Lechange endpoints documented by the skill and review the value before execution.

Risk: The requests dependency is specified as an open version range.

Mitigation: Use a pinned or locked dependency installation and scan the resolved environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imou-openplatform/skills/imou-device-video)
- [Publisher profile](https://clawhub.ai/user/imou-openplatform)
- [Imou Open API Reference - Device Video](artifact/references/imou-video-api.md)
- [Imou development specification](https://open.imoulife.com/book/http/develop.html)
- [Imou accessToken API](https://open.imou.com/document/pages/fef620/)
- [Imou bindDeviceLive API](https://open.imou.com/document/pages/1bc396/)
- [Imou createDeviceRecordHls API](https://open.imou.com/document/pages/185646/)
- [Imou liveList API](https://open.imou.com/document/pages/b0e047/)
- [Imou queryLocalRecords API](https://open.imou.com/document/pages/396dce/)
- [Imou queryCloudRecords API](https://open.imou.com/document/pages/8e0e35/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include sensitive HLS URLs and record metadata returned by the configured Imou Open API endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
