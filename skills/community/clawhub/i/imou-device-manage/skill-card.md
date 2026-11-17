## Description:

Lists and manages Imou cloud devices, including device lists, serial lookup, device and channel details, and device or channel renaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imou-openplatform](https://clawhub.ai/user/imou-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to query Imou account devices, inspect device and channel status, and rename devices or channels through the Imou Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, tokens, and device data may be sent to a configured API URL that is not verified by the skill.

Mitigation: Set IMOU_BASE_URL only to an official Imou HTTPS API endpoint for the intended region and review the environment before running the skill.

Risk: The rename command changes cloud device or channel metadata.

Mitigation: Confirm the target serial, optional channel ID, and new name before executing rename operations.

Risk: App IDs, app secrets, access tokens, device serials, names, and status data are sensitive.

Mitigation: Store credentials in a trusted environment and avoid sharing command output or JSON results where unauthorized users can access them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imou-openplatform/skills/imou-device-manage)
- [Imou Open API Reference - Device Management](references/imou-device-api.md)
- [Imou Development Specification](https://open.imou.com/document/pages/c20750/)
- [Get Access Token API](https://open.imou.com/document/pages/fef620/)
- [List Devices by Page API](https://open.imou.com/document/pages/683248/)
- [Get Devices by IDs API](https://open.imou.com/document/pages/320fb7/)
- [Modify Device or Channel Name API](https://open.imou.com/document/pages/8ffaa3/)
- [Overseas Development Specification](https://open.imoulife.com/book/http/develop.html)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and optional JSON, with Markdown guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMOU_APP_ID and IMOU_APP_SECRET; IMOU_BASE_URL selects the Imou API endpoint.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
