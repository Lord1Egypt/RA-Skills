## Description:

Imou/Lechange device operation for PTZ control, snapshot capture, and image download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imou-openplatform](https://clawhub.ai/user/imou-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control Imou or Lechange cameras through the Imou Open API, including PTZ movement and snapshot capture or download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive camera tokens and device data can be sent to an unvalidated network endpoint if IMOU_BASE_URL is misconfigured.

Mitigation: Use only documented HTTPS Imou API base URLs and keep IMOU_APP_SECRET private.

Risk: Camera snapshots and PTZ movement can expose privacy-sensitive scenes or physically move a camera.

Mitigation: Require user authorization before snapshot capture, image download, or PTZ movement.

Risk: The --save option can write content from unexpected snapshot responses before URL and file-size validation is added.

Mitigation: Avoid --save on untrusted or unexpected snapshot responses and inspect snapshot URLs before downloading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imou-openplatform/skills/imou-device-operate)
- [Imou Open API reference summary](references/imou-operate-api.md)
- [Imou developer portal](https://open.imou.com)
- [Imou overseas developer portal](https://open.imoulife.com)
- [Imou development specification](https://open.imoulife.com/book/http/develop.html)
- [Get accessToken API](https://open.imou.com/document/pages/fef620/)
- [Device snapshot API](https://open.imou.com/document/pages/09fe83/)
- [PTZ move control API](https://open.imou.com/document/pages/66c489/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output, URLs, and optional downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot URLs are time-limited by the upstream API; optional local downloads write image files to the requested path.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
