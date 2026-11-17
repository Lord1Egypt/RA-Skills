## Description:

Analyzes Imou device snapshots or image URLs with Imou Open API for scene detections, heatmap statistics, face analysis, and detect repository or target management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imou-openplatform](https://clawhub.ai/user/imou-openplatform)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run Imou Open API image analysis on device snapshots or accessible image URLs and to manage detect repositories and targets for workwear, absence, heatmap, and face workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive face, workwear, surveillance, or Base64 image data may be submitted to the configured Imou Open API endpoint.

Mitigation: Treat image inputs as sensitive and use the skill only with approved Imou accounts, data centers, and data handling policies.

Risk: A custom or HTTP IMOU_BASE_URL can direct credentials and image data to an unintended API destination.

Mitigation: Set IMOU_BASE_URL only to official Imou HTTPS base URLs for the intended region.

Risk: Repository and target deletion commands can remove Imou detect assets.

Mitigation: Confirm repository IDs and target IDs before deletion and prefer limited-scope credentials.

Risk: The requests dependency is not pinned to an exact version.

Mitigation: Use a reviewed lockfile or pinned dependency version before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imou-openplatform/skills/imou-multimodal-analysis)
- [Imou Open API Reference - AI Multimodal Analysis](references/imou-ai-api.md)
- [Imou Open Platform](https://open.imou.com)
- [Imou Overseas Open Platform](https://open.imoulife.com)
- [Imou Development Specification](https://open.imoulife.com/book/http/develop.html)
- [Imou AI Overview](https://open.imou.com/document/pages/f1b9a3/)
- [Imou Get Access Token](https://open.imou.com/document/pages/fef620/)
- [Imou Human Detection API](https://open.imou.com/document/pages/93rflk/)
- [Imou Face Analysis API](https://open.imou.com/document/pages/28d7ug/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Imou credentials and may submit image URLs, Base64 image data, repository IDs, thresholds, and detection regions to the configured Imou Open API base URL.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
