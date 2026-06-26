## Description: <br>
Analyzes Imou device snapshot or image URLs for people, behaviors, workwear and absence, shelf and trash status, heatmap data, and face signals, and helps manage Imou AI detection repositories and targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Imou-OpenPlatform](https://clawhub.ai/user/Imou-OpenPlatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run Imou Open API image analysis on device snapshots or image URLs and maintain detection repositories or target images for workflows such as workwear, absence, shelf, trash, heatmap, and face analysis. <br>

### Deployment Geography for Use: <br>
Global, subject to selecting the appropriate Imou regional IMOU_BASE_URL and applicable Imou account or data-center terms. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected camera or image data and Imou credentials to the configured Imou Open API endpoint. <br>
Mitigation: Use dedicated least-privilege Imou developer credentials, send only intended images, and choose the correct regional IMOU_BASE_URL. <br>
Risk: Repository and target delete commands can remove Imou AI detection resources. <br>
Mitigation: List repositories or targets first, verify IDs before deleting, and test with non-production resources where possible. <br>
Risk: Credential exposure could grant access to Imou API operations supported by the account. <br>
Mitigation: Keep credentials in environment variables or a secret manager, avoid logging them, and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Imou-OpenPlatform/imou-multimodal-analysis) <br>
- [Imou Open API Reference - AI Multimodal Analysis](references/imou-ai-api.md) <br>
- [Imou AI overview](https://open.imou.com/document/pages/f1b9a3/) <br>
- [Imou development specification](https://open.imou.com/document/pages/c20750/) <br>
- [Imou accessToken API](https://open.imou.com/document/pages/fef620/) <br>
- [Imou overseas development specification](https://open.imoulife.com/book/http/develop.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI executions return JSON or status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IMOU_APP_ID, IMOU_APP_SECRET, and optional IMOU_BASE_URL environment variables; image input may be a URL or base64 payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
