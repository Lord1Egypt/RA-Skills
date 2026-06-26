## Description: <br>
Provides Imou/Lechange device video access for live HLS streams, local and cloud record clip queries, and playback HLS URLs by device channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imou-openplatform](https://clawhub.ai/user/imou-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing Imou/Lechange cameras use this skill to obtain live stream URLs, query recorded clips, and create playback URLs for a specific device channel. <br>

### Deployment Geography for Use: <br>
Global, subject to Imou regional API endpoint availability. <br>

## Known Risks and Mitigations: <br>
Risk: Imou app credentials and access tokens are sensitive and are used to request live streams and playback URLs. <br>
Mitigation: Store credentials in trusted environment variables, avoid logging secrets or returned tokens, and rotate credentials if they are exposed. <br>
Risk: The skill sends device identifiers, channel identifiers, time ranges, and access tokens to the configured Imou Open API endpoint. <br>
Mitigation: Verify IMOU_BASE_URL before use, choose the correct regional endpoint, and run the skill only in environments approved for the target devices. <br>
Risk: Returned HLS and playback URLs can expose live or recorded camera video while they remain valid. <br>
Mitigation: Share returned URLs only with authorized users and use playback URLs promptly because the artifact notes limited validity. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imou-openplatform/imou-device-video) <br>
- [Imou Open API Reference - Device Video](references/imou-video-api.md) <br>
- [Imou Developer Specification](https://open.imou.com/document/pages/c20750/) <br>
- [Imou accessToken API](https://open.imou.com/document/pages/fef620/) <br>
- [Imou bindDeviceLive API](https://open.imou.com/document/pages/1bc396/) <br>
- [Imou createDeviceRecordHls API](https://open.imou.com/document/pages/185646/) <br>
- [Imou liveList API](https://open.imou.com/document/pages/b0e047/) <br>
- [Imou queryLocalRecords API](https://open.imou.com/document/pages/396dce/) <br>
- [Imou queryCloudRecords API](https://open.imou.com/document/pages/8e0e35/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text HLS URLs, JSON record data, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Imou app credentials and a configured regional API base URL; playback URLs have limited validity.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
